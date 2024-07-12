"""
modules/utils.py

Utility functions for handling various tasks like space checking, trailer pulling, and downloading.
"""

import os
import shutil
import subprocess
import re
from datetime import datetime, timezone
import requests
import yt_dlp
import urllib3
from modules.logger import Logger

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Utils:
    def __init__(self, logger: Logger, config: list) -> None:
        """
        Initialize Utils class with a logger and configuration.

        :param logger: Logger instance for logging messages
        :param config: Configuration dictionary or list
        """
        self.logger = logger
        self.config = config

    def replace_slash_backslash(self, text: str) -> str:
        """
        Replace forward slashes and backward slashes with spaces.
        Replace multiple spaces with a single space.

        :param text: Input text containing slashes
        :return: Text with replaced slashes and spaces
        """
        text = re.sub(r"[\\/]+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def trailer_pull(self, tmdb_id: str, item_type: str, parent_mode=False) -> list:
        """
        Retrieve trailer information from TMDB API.

        :param tmdb_id: TMDB ID of the movie or TV show
        :param item_type: Type of item ('movie' or 'tv')
        :param parent_mode: Flag for parent mode retrieval (TV)
        :return: List of cleaned trailer information
        """
        # Log the process of getting trailer information
        self.logger.info(
            "\t\t -> GET",
            "Getting information about {tmdb_id} {item_type}",
            tmdb_id=tmdb_id,
            item_type=str(item_type).upper(),
        )
        base_link = "api.themoviedb.org/3"
        api_key = self.config["tmdb_api"]

        # Construct the URL for TMDB API based on item type and TMDB ID
        url = f"https://{base_link}/{item_type}/{tmdb_id}/videos"
        if parent_mode:
            url = f"https://{base_link}/find/{tmdb_id}?external_source=imdb_id"

        headers = {"accept": "application/json"}

        # Make a GET request to TMDB API
        response = requests.get(
            url,
            params={
                "api_key": api_key,
                "language": self.config["default_language_trailer"],
            },
            headers=headers,
            timeout=3000,
            verify=False,
        )

        # Process the response from TMDB API
        if 200 >= response.status_code <= 300:
            raw_trailers = response.json()
            if parent_mode:
                return raw_trailers.get("tv_results", [])

            raw_trailers = raw_trailers.get("results", [])
            trailers = []
            # Extract relevant trailer information from the API response
            for trailer in raw_trailers:
                if (
                    trailer.get("official") == self.config["TMDB_official"]
                    and trailer.get("type") in self.config["TMDB_type_of_trailler"]
                    and trailer.get("size") == self.config["TMDB_size"]
                    and trailer.get("site") == self.config["TMDB_source"]
                ):
                    trailer["yt_link"] = self.config["yt_link_base"] + trailer["key"]
                    trailer["name"] = self.replace_slash_backslash(trailer["name"])
                    # Parse the published_at string to a datetime object with UTC timezone
                    trailer["published_at"] = datetime.strptime(
                        trailer["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ"
                    ).replace(tzinfo=timezone.utc)
                    trailers.append(trailer)

            # Sort the list based on the proximity to the current datetime
            trailers = sorted(
                trailers,
                key=lambda x: abs(datetime.now(timezone.utc) - x["published_at"]),
            )
            return trailers

        # Handle warnings if the response status code is not in the 200-300 range
        self.logger.warning(
            "[ TMDB ]",
            "{msg_gen}",
            msg_gen=f"{response.status_code} - {response.json()['status_message']}",
        )
        return []

    def post_process(self, cache_path: str, files: str, item: dict) -> None:
        """
        Post-processing function for downloaded files using FFMPEG.

        :param cache_path: Path to downloaded files cache
        :param files: List of downloaded files
        :param item_path: Path to the item's directory
        """

        # Log the process of post-processing downloaded files
        self.logger.info(
            "\t\t -> POST PROCESS",
            "Create '{path}' folder",
            path=item["outputs_folder"],
        )

        os.makedirs(item["outputs_folder"], exist_ok=True)

        # Iterate through each downloaded file and perform FFMPEG processing
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            filetype = self.config["filetype"]
            msg_gen = [
                "ffmpeg",
                "-i",
                f"{cache_path}/{file}",
                "-threads",
                str(self.config["thread_count"]),
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-af",
                "volume=-7dB",
                "-bufsize",
                self.config["buffer_size_ffmpeg"],
                "-preset",
                "slow",
                "-y",
                f"{item['outputs_folder']}/{filename}.{filetype}",
            ]
            # Log the FFMPEG command used for processing
            self.logger.info("\t\t -> FFMPEG", "{msg_gen}", msg_gen=" ".join(msg_gen))
            # Execute the FFMPEG command with subprocess
            if self.config["quiet_mode"]:
                with open(os.devnull, "wb") as output:
                    subprocess.run(
                        msg_gen, stdout=output, stderr=output, stdin=output, check=False
                    )
            else:
                subprocess.run(msg_gen, check=False)

    def yt_dlp_process(self, link: str, ytdl_opts: dict) -> None:
        """
        Download trailer using yt-dlp.

        :param link: Trailer link information
        :param ytdl_opts: Options for yt-dlp
        """
        ydl = yt_dlp.YoutubeDL(ytdl_opts)
        try:
            # Log the process of downloading the trailer using yt-dlp
            self.logger.info(
                "\t\t -> DOWNLOAD",
                "Downloading {title} trailer from {link}",
                title=link["name"],
                link=link["yt_link"],
            )
            ydl.download([link["yt_link"]])
        except yt_dlp.DownloadError as e:
            # Handle yt-dlp download errors and log them
            self.logger.error(
                "\t\t -> DOWNLOAD",
                "Failed to download from {link}: {error}",
                link=link["name"],
                error=e,
            )
        except ValueError as e:
            # Handle invalid value errors during yt-dlp download and log them
            self.logger.error(
                "\t\t -> DOWNLOAD",
                "Invalid duration for {link}: {error}",
                link=link["name"],
                error=e,
            )

    def trailer_download(self, links: list, item: dict) -> None:
        """
        Download trailers from YouTube.

        :param links: List of YouTube trailer links
        :param item: Metadata of the item (movie or TV show)
        """
        cache_path = f'cache/{item["title"]}'
        os.makedirs(cache_path, exist_ok=True)

        def dl_progress(d):
            # Define a download progress function to handle yt-dlp progress hooks
            if d["status"] == "finished":
                self.logger.success("\t\t -> DOWNLOAD", "Trailer downloaded.")
            elif d["status"] == "error":
                self.logger.error("\t\t -> DOWNLOAD", "Trailer download failed.")

        ytdl_opts = {
            "progress_hooks": [dl_progress],
            "format": "bestvideo+bestaudio",
            "username": self.config["auth_yt_user"],
            "password": self.config["auth_yt_pass"],
            "no_warnings": self.config["no_warnings"],
            "outtmpl": f'{cache_path}/{item["sortTitle"]}',
            "sleep_interval_requests": self.config['YT_DLP_sleep_interval_requests'],
        }
        if self.config.get("quiet_mode", False):
            ytdl_opts["quiet"] = True
            ytdl_opts["noprogress"] = True

        if self.config["skip_intros"]:
            ytdl_opts["postprocessors"] = [
                {"key": "SponsorBlock"},
                {
                    "key": "ModifyChapters",
                    "remove_sponsor_segments": self.config[
                        "YT_DLP_remove_spensors_block"
                    ],
                },
            ]

        def check_duration(i: dict, **info: any) -> Exception:
            # Define a duration check function for trailers
            duration = info.get("duration")
            max_length = self.config["max_length"]
            if duration and (int(duration) > int(max_length)):
                raise ValueError(
                    "Invalid duration for {link}: {error}".format(
                        link=i["name"], error=f"{duration}s"
                    )
                )

        for link in links:
            if self.config["only_one_trailer"] and len(os.listdir(cache_path)) == 1:
                continue
            if self.config["max_length"]:
                ytdl_opts["match_filter"] = lambda info: check_duration(link, **info)
            try:
                ytdl_opts["outtmpl"] = f"{cache_path}/{link['name']}"
                self.yt_dlp_process(link, ytdl_opts)
            except Exception as e:
                self.logger.info(f"fail to download {link} {e}")
                continue

        if os.path.exists(cache_path):
            files = os.listdir(cache_path)
            if len(files) > 0:
                self.post_process(cache_path, files, item)
            shutil.rmtree(cache_path)
        else:
            self.logger.error(
                "\t\t -> DOWNLOAD",
                "No cache folder for {title}",
                title=item["title"],
            )

    def check_space(self, path: str) -> bool:
        """
        Check available disk space at the given path.

        :param path: Path to check for available disk space
        :return: True if disk space is sufficient, False otherwise
        """
        min_free_gb = self.config.get(
            "min_free_space_gb", 5
        )  # Minimum free space required in GB
        _, _, free = shutil.disk_usage(path)
        free_gb = free / (1024**3)  # Convert bytes to GB
        if free_gb < min_free_gb:
            self.logger.error(
                "DISK SPACE",
                "Insufficient disk space in {path}. Only {free_gb:.2f} GB free.",
                path=path,
                free_gb=free_gb,
            )
            return False
        return True

    def check_existing_trailer(self, trailers: list, existing_trailers: list) -> list:
        """
        Check if trailers already exist for the given movie or TV show.

        :param trailers: List of trailers to check
        :param existing_trailers: List of existing trailers
        :return: List of trailers that need to be downloaded
        """
        new_download = []
        # Compare new trailers with existing ones and determine which ones need to be downloaded
        for trailer in trailers:
            if trailer["name"] not in existing_trailers:
                new_download.append(trailer)
        return new_download
