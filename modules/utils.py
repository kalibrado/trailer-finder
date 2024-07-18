"""
Module providing utility functions for handling trailers, downloading from YouTube, and post-processing with FFMPEG.

This module contains utility functions to handle trailers, download them from YouTube using `yt-dlp`, post-process
using FFMPEG, and perform disk space checks. It integrates with configurations from `config.yaml` to customize behavior
like search prefixes, custom paths, and API keys.

Dependencies:
    - os: Operating system interface for file operations.
    - shutil: High-level file operations utility.
    - re: Regular expression operations for string manipulation.
    - datetime: Date and time handling.
    - subprocess: Subprocess management for executing FFMPEG commands.
    - requests: HTTP library for making requests to external APIs.
    - urllib3: HTTP client utility for disabling SSL warnings.
    - modules.logger.Logger: Logger instance for logging messages.
    - modules.youtube_dl.YoutubeDL: Class for downloading trailers using `yt-dlp`.
    - modules.exceptions.FfmpegError: Exception raised for errors during FFMPEG processing.
    - modules.exceptions.FfmpegCommandMissing: Exception raised when FFMPEG command is not defined in `config.yaml`.
    - modules.exceptions.InsufficientDiskSpaceError: Exception raised when there is insufficient disk space.

Classes:
    - Utils(Translator):
        Class providing utility functions for handling trailers, downloading from YouTube, and post-processing with FFMPEG.

Attributes:
    logger (Logger): Logger instance for logging messages.
    config (dict): Configuration dictionary containing settings from `config.yaml`.
    yt_downloader (YoutubeDL): Instance of YoutubeDL for downloading trailers using `yt-dlp`.

Usage:
    This module provides essential utility functions for handling trailers, downloading from YouTube,
    post-processing with FFMPEG, and performing disk space checks. It integrates with `config.yaml`
    for customized behavior and settings. Ensure configurations are set correctly before using these functions.
"""

import os
import shutil
import re
from datetime import datetime, timezone
import subprocess
from typing import List, Dict, Union
import requests
import urllib3
from modules.logger import Logger
from modules.youtube_dl import YoutubeDL
from modules.exceptions import FfmpegError, FfmpegCommandMissing, InsufficientDiskSpaceError
from modules.translator import Translator

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Utils(Translator):
    def __init__(self, logger: Logger, config: Dict[str, Union[str, int, bool, list]]) -> None:
        """
        Initialize Utils class with a logger and configuration.

        :param logger: Logger instance for logging messages
        :param config: Configuration dictionary or list
        """
        self.logger = logger
        self.config = config
        self.yt_downloader = YoutubeDL(logger, config)
        super().__init__(config.get("APP_TRANSLATE"))

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

    def get_title(self, item: Dict[str, str]) -> str:
        """
        Get the title of an item from its metadata.

        :param item: Metadata dictionary of the item
        :return: Title of the item
        """
        # Using self.config.get with a default value
        title_key = self.config.get("APP_USE_TITLE", "title")

        title = item["title"]

        # Check if title_key contains "title" (case insensitive)
        if "title" in title_key.lower():
            title = item.get(title_key, item["title"])

        return title

    def trailer_pull(self, tmdb_id: str, item_type: str, item: dict, seasonNumber=None) -> List[Dict[str, Union[str, bool, datetime]]]:
        """
        Retrieve trailer information from TMDB API.

        :param tmdb_id: TMDB ID of the movie or TV show
        :param item_type: Type of item ('movie' or 'tv')
        :param seasonNumber: Season number (for TV shows)
        :param item: Metadata of the item
        :return: List of cleaned trailer information
        """

        base_link = "api.themoviedb.org/3"
        api_key = self.config["TMDB_API_KEY"]

        if seasonNumber:
            url = f"https://{base_link}/tv/{tmdb_id}/season/{seasonNumber}/videos"
        else:
            url = f"https://{base_link}/{item_type}/{tmdb_id}/videos"

        headers = {"accept": "application/json"}
        self.logger.info("Retrieving information about « {info} ».", info=url)

        try:
            response = requests.get(
                url,
                params={
                    "api_key": api_key,
                    "language": self.config["TMDB_LANGUAGE_TRAILER"],
                },
                headers=headers,
                timeout=3000,
                verify=False,
            )
            response.raise_for_status()

            trailers = []
            raw_trailers = response.json()

            for trailer in raw_trailers.get("results", []):
                if self._should_add_trailer(trailer):
                    trailer_data = {
                        "query_type": f"API (TMDB) {url}",
                        "yt_link": self.config["YT_DLP_BASE_URL"] + trailer["key"],
                        "name": self.replace_slash_backslash(trailer["name"]),
                        "published_at": datetime.strptime(trailer["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc),
                    }
                    trailers.append(trailer_data)

            if self.config.get("APP_ONLY_ONE_TRAILER", False):
                trailers.sort(key=lambda x: abs(datetime.now(timezone.utc) - x["published_at"]))

            return trailers

        except (requests.RequestException, ValueError) as e:
            self.logger.error("Failed to retrieve trailers from TMDB API: {error}", error=str(e))
            return []

    def _should_add_trailer(self, trailer: dict) -> bool:
        """
        Determine if a trailer should be added based on configured conditions.

        :param trailer: Dictionary containing trailer information
        :return: True if the trailer meets all conditions, False otherwise
        """
        conditions = [
            (self.config.get("TMDB_OFFICIAL", True), lambda x: x.get("official", False) == self.config.get("TMDB_OFFICIAL", True)),
            (self.config.get("TMDB_TYPE_ITEM", None), lambda x: x.get("type") in self.config.get("TMDB_TYPE_ITEM", None)),
            (self.config.get("TMDB_SIZE", None), lambda x: x.get("size") == self.config.get("TMDB_SIZE", None)),
            (self.config.get("TMDB_SOURCE", None), lambda x: x.get("site") == self.config.get("TMDB_SOURCE", None)),
        ]

        return all(condition[0] is None or condition[1](trailer) for condition in conditions)

    def post_process(self, cache_path: str, files: List[str], item: Dict[str, str]) -> None:
        """
        Perform post-processing on downloaded trailers using FFMPEG.

        :param cache_path: Path to the cache directory containing trailers
        :param files: List of downloaded trailer filenames
        :param item: Metadata of the item (movie or TV show)
        """
        trailers_path = os.path.join(item["path"], "trailers")
        os.makedirs(trailers_path, exist_ok=True)

        ffmpeg_cmd_template = self.config.get("FFMPEG_COMMAND_TEMPLATE", None)
        if ffmpeg_cmd_template is None:
            raise FfmpegCommandMissing(self.translate("The ffmpeg command is not defined in config.yaml."))

        # Iterate through each downloaded file and perform FFMPEG processing
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            filetype = self.config.get("FFMPEG_FILE_TYPE", "mkv")

            cmd = ffmpeg_cmd_template.format(
                path=f"{cache_path}/{file}",
                thread=self.config.get("FFMPEG_THREAD_COUNT", 4),
                buffer=self.config.get("FFMPEG_BUFFER_SIZE", "1M"),
                path_file=f"{item['trailers_dest']}/{filename}.{filetype}",
            )

            # Log the FFMPEG command used for processing
            self.logger.info("ffmpeg command « {cmd} ».", cmd=cmd)

            subprocess_args = {}
            if self.config.get("APP_QUIET_MODE", False):
                subprocess_args["stdout"] = subprocess.DEVNULL
                subprocess_args["stderr"] = subprocess.DEVNULL
                subprocess_args["stdin"] = subprocess.DEVNULL

            try:
                # Execute the FFMPEG command with subprocess
                subprocess.run(cmd, **subprocess_args, check=False, shell=True)
            except subprocess.CalledProcessError as e:
                raise FfmpegError(self.translate("The ffmpeg command has an error « {error} ».", error=e))
        # Always remove the cache_path after FFMPEG execution
        shutil.rmtree(cache_path)

    def download_trailers(self, links: List[dict], item: Dict[str, str]) -> None:
        """
        Download trailers from YouTube using YoutubeDL.

        :param links: List of YouTube trailer links
        :param item: Metadata of the item (movie or TV show)
        """

        prefix_search = self.config.get("YT_SEARCH_PREFIX", [])

        arr_id_trailer = item.get("youTubeTrailerId", None)
        if arr_id_trailer:
            link = {
                "name": self.replace_slash_backslash(self.get_title(item)),
                "yt_link": self.config["YT_DLP_BASE_URL"] + arr_id_trailer,
                "query_type": f"*arr youTube id: {arr_id_trailer}",
            }
            links.append(link)

        for prefix in prefix_search:
            link = {
                "name": self.replace_slash_backslash(self.get_title(item)),
                "yt_link": f"{prefix}:{item['use_title']} {self.config.get('YT_DLP_SEARCH_KEYWORD', '')}",
                "query_type": f"prefix: {prefix}",
            }
            links.append(link)

        cache_path = self.yt_downloader.download_trailers(links, item)

        if os.path.exists(cache_path):
            files = os.listdir(cache_path)
            if len(files) > 0:
                self.post_process(cache_path, files, item)
                return

    def check_space(self, path: str) -> bool:
        """
        Check available disk space to ensure there is enough space to download and process trailers.

        :param path: Path where trailers will be downloaded
        :return: Boolean indicating if there is enough space
        """

        total, used, free = shutil.disk_usage(path)
        free_gb = free / (1024**3)  # Convert bytes to GB
        if free_gb < self.config.get("APP_FREE_SPACE_GB", 5):
            raise InsufficientDiskSpaceError(
                self.translate(
                    "« {path} » does not have enough disk space. Only « {free_gb} » GB are available.",
                    path=path,
                    free_gb=int(free_gb),
                )
            )

    def get_new_trailers(self, trailer_names: List[str], existing_files: List[str]) -> List[str]:
        """
        Get trailer names that do not already exist in the specified folder.

        :param trailer_names: List of trailer names to check
        :param existing_files: Files existing
        :return: List of trailer names that do not already exist in the folder
        """
        existing_names = [os.path.splitext(file)[0] for file in existing_files]

        new_trailers = []
        for name in trailer_names:
            if name not in existing_names:
                new_trailers.append(name)

        return new_trailers
