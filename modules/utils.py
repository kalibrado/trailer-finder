"""
Module providing utility functions for handling trailers, downloading from YouTube, and post-processing with FFMPEG.

This module includes classes and functions for interacting with TMDB API, downloading trailers, and performing
post-processing using FFMPEG.

Classes:
    - Utils: Contains utility methods for trailer handling, downloading, and processing.

Functions:
    - replace_slash_backslash: Replaces forward slashes and backward slashes with spaces.
    - get_title: Retrieves the title of an item from its metadata.
    - trailer_pull: Retrieves trailer information from TMDB API.
    - post_process: Performs post-processing on downloaded trailers using FFMPEG.
    - download_trailers: Downloads trailers from YouTube using YoutubeDL.
    - check_space: Checks available disk space for downloading and processing trailers.
    - get_new_trailers: Retrieves trailer names that do not already exist in the specified folder.
Example of usage:

# Importing Logger class and Utils module
from modules.logger import Logger
from modules.utils import Utils

# Initializing the logger
logger = Logger()
config = {
    "RADARR_USE_NAME": "originalTitle",
    "TMDB_API_KEY": "your_tmdb_api_key_here",
    # Other configurations here...
}

# Initializing an instance of Utils
utils = Utils(logger, config)

# Example usage to download trailers
tmdb_id = "12345"
item_type = "movie"

# Fetching trailer information from TMDB
trailers = utils.trailer_pull(tmdb_id, item_type)

# Downloading trailers from YouTube
item_metadata = {
    "title": "Your Movie Title",
    "year": 2024,
    "path": "/path/to/movie",
    "outputs_folder": "/path/to/output/folder",
    # Other metadata here...
}
utils.download_trailers(trailers, item_metadata)

# Checking available disk space before download
download_path = "/path/to/download/trailers"
has_enough_space = utils.check_space(download_path)

if not has_enough_space:
    print("Insufficient disk space. Unable to download trailers.")

# Example usage to perform post-processing on downloaded trailers
cache_path = "/path/to/cache/trailers"
downloaded_files = ["trailer1.mp4", "trailer2.mp4", "trailer3.mp4"]
utils.post_process(cache_path, downloaded_files, item_metadata)

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

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Utils:
    def __init__(self, logger: Logger, config: Dict[str, Union[str, int, bool]]) -> None:
        """
        Initialize Utils class with a logger and configuration.

        :param logger: Logger instance for logging messages
        :param config: Configuration dictionary or list
        """
        self.logger = logger
        self.config = config
        self.yt_downloader = YoutubeDL(logger, config)

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

    def trailer_pull(self, tmdb_id: str, item_type: str, seasonNumber=None) -> List[Dict[str, Union[str, bool, datetime]]]:
        """
        Retrieve trailer information from TMDB API.

        :param tmdb_id: TMDB ID of the movie or TV show
        :param item_type: Type of item ('movie' or 'tv')
        :param parent_mode: Flag for parent mode retrieval (TV)
        :return: List of cleaned trailer information
        """
        # Log the process of getting trailer information
        self.logger.info("\t\t ->", "Getting information about {info}", info=f"TYPE: {item_type} ID: {tmdb_id}")
        base_link = "api.themoviedb.org/3"
        api_key = self.config["TMDB_API_KEY"]

        # Construct the URL for TMDB API based on item type and TMDB ID
        url = f"https://{base_link}/{item_type}/{tmdb_id}/videos"
        if seasonNumber:
            url = f"https://{base_link}/tv/{tmdb_id}/season/{seasonNumber}/videos"

        headers = {"accept": "application/json"}

        # Make a GET request to TMDB API
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

        # Process the response from TMDB API
        if 200 <= response.status_code < 300:
            raw_trailers = response.json()
            assert isinstance(raw_trailers, dict)

            trailers = []
            # Extract relevant trailer information from the API response
            for trailer in raw_trailers.get("results", []):
                # Check if the trailer meets the specified conditions
                should_add_trailer = True

                # Verify each condition only if it is present in the configuration
                if self.config.get("TMDB_OFFICIAL", True):
                    should_add_trailer = should_add_trailer and (trailer.get("official") == self.config.get("TMDB_OFFICIAL", True))

                if self.config.get("TMDB_TYPE_ITEM", None):
                    should_add_trailer = should_add_trailer and (trailer.get("type") in self.config.get("TMDB_TYPE_ITEM", None))

                if self.config.get("TMDB_SIZE", None):
                    should_add_trailer = should_add_trailer and (trailer.get("size") == self.config.get("TMDB_SIZE", None))

                if self.config.get("TMDB_SOURCE", None):
                    should_add_trailer = should_add_trailer and (trailer.get("site") == self.config.get("TMDB_SOURCE", None))

                # If all specified conditions are met, process the trailer
                if should_add_trailer:
                    # Construct the YouTube link for the trailer using the base link
                    # from the config and the trailer's key.
                    trailer["yt_link"] = self.config["YT_DLP_BASE_URL"] + trailer["key"]
                    # Replace any backslashes or forward slashes in the trailer's name.
                    trailer["name"] = self.replace_slash_backslash(trailer["name"])
                    # Parse the 'published_at' string to a datetime object with UTC timezone.
                    trailer["published_at"] = datetime.strptime(trailer["published_at"], "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)
                    # Add the trailer to the list of trailers.
                    trailers.append(trailer)

            # Sort the list based on the proximity to the current datetime
            if self.config.get("APP_ONLY_ONE_TRAILER", False):
                trailers = sorted(
                    trailers,
                    key=lambda x: abs(datetime.now(timezone.utc) - x["published_at"]),
                )

            return trailers

        # Handle warnings if the response status code is not in the 200-300 range
        msg = f"{response.status_code} - {response.json().get('status_message', 'No message')}"
        self.logger.warning("\t\t ->", "Warning: {warning}", warning=msg)
        return []

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
            raise ValueError("FFMPEG Template commande not definned")

        # Iterate through each downloaded file and perform FFMPEG processing
        for file in files:
            filename = os.path.splitext(os.path.basename(file))[0]
            filetype = self.config.get("FFMPEG_FILE_TYPE", "mkv")

            cmd = ffmpeg_cmd_template.format(
                path=f"{cache_path}/{file}",
                thread=self.config.get("FFMPEG_THREAD_COUNT", 4),
                buffer=self.config.get("FFMPEG_BUFFER_SIZE", "1M"),
                path_file=f"{item['outputs_folder']}/{filename}.{filetype}",
            )

            # Log the FFMPEG command used for processing
            self.logger.info("\t\t ->", "FFMPEG Run commande: {cmd}", cmd=cmd)

            subprocess_args = {}
            if self.config.get("APP_QUIET_MODE", False):
                subprocess_args["stdout"] = subprocess.DEVNULL
                subprocess_args["stderr"] = subprocess.DEVNULL
                subprocess_args["stdin"] = subprocess.DEVNULL

            # Execute the FFMPEG command with subprocess
            subprocess.run(cmd, **subprocess_args, check=False, shell=True)

        # Always remove the cache_path after FFMPEG execution
        shutil.rmtree(cache_path)

    def download_trailers(self, links: List[str], item: Dict[str, str]) -> None:
        """
        Download trailers from YouTube using YoutubeDL.

        :param links: List of YouTube trailer links
        :param item: Metadata of the item (movie or TV show)
        """
        cache_path = self.yt_downloader.download_trailers(links, item)

        # Perform post-processing on downloaded files
        if os.path.exists(cache_path):
            files = os.listdir(cache_path)
            if not files:
                name = self.get_title(item)
                self.logger.warning("\t\t ->", "No trailers available on {query}", query=item["query_type"])

                link = {
                    "name": self.replace_slash_backslash(name),
                    "yt_link": f"ytsearch5:{item['use_title']} ({item['year']}) {self.config.get('YT_DLP_SEARCH_KEYWORD')}",
                }

                arr_id_trailer = item.get("youTubeTrailerId", None)
                if arr_id_trailer:
                    link["yt_link"] = self.config["YT_DLP_BASE_URL"] + arr_id_trailer
                item["query_type"] = link["yt_link"]

                self.logger.info("\t\t ->", "Search trailer with {query}", query=item["query_type"])
                cache_path = self.yt_downloader.download_trailers([link], item)
                files = os.listdir(cache_path)

            if len(files) > 0:
                self.post_process(cache_path, files, item)

    def check_space(self, path: str) -> bool:
        """
        Check available disk space to ensure there is enough space to download and process trailers.

        :param path: Path where trailers will be downloaded
        :return: Boolean indicating if there is enough space
        """
        disk = shutil.disk_usage(path)
        # Convert GB to bytes
        min_free_space = self.config.get("MIN_FREE_SPACE", 10) * (1024**3)
        return disk.free > min_free_space

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
