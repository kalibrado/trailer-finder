"""
Module providing utility functions for handling trailers, downloading from YouTube, and post-processing with FFMPEG.

This module contains utility functions to interact with YouTube's API using `yt-dlp`, download trailers, and perform
post-processing tasks using FFMPEG. It leverages configurations from `config.yaml` to customize behavior such as
download formats, interval requests, and error handling.

Dependencies:
    - os: Operating system interface for file operations.
    - yt_dlp: Library for downloading videos from YouTube.
    - modules.logger.Logger: Logger instance for logging messages.
    - modules.exceptions.DurationError: Exception raised when trailer duration exceeds the maximum length.
    - modules.exceptions.DownloadError: Exception raised for errors during trailer downloads.
    - modules.translator.Translator: Translator class for translating messages.

Classes:
    - YoutubeDL(Translator):
        Class providing methods to handle trailer downloads from YouTube using yt-dlp.

Attributes:
    logger (Logger): Logger instance for logging messages.
    config (dict): Configuration dictionary containing settings from `config.yaml`.

Usage:
    This module provides essential functions for downloading trailers from YouTube, processing them with FFMPEG,
    and interacting with external APIs like TMDB. Ensure `config.yaml` is configured correctly with relevant API keys
    and settings before running scripts that use these functions.
"""

import os
import yt_dlp
from modules.logger import Logger
from modules.exceptions import DurationError, DownloadError
from modules.translator import Translator


class YoutubeDL(Translator):
    def __init__(self, logger: Logger, config: dict) -> None:
        """
        Initialize YoutubeDL class with a logger and configuration.

        :param logger: Logger instance for logging messages
        :param config: Configuration dictionary or list
        """
        self.logger = logger
        self.config = config
        super().__init__(config.get("APP_TRANSLATE"))

    def progress_hooks(self, d: dict):
        info_dict = d.get("info_dict")
        title = d["filename"].split("/")[-1]
        if isinstance(info_dict, dict):
            title = info_dict.get("title")
        # Define a download progress function to handle yt-dlp progress hooks
        if d["status"] == "finished":
            self.logger.success("The download of the trailer « {title} » succeeded.", title=title)
        if d["status"] == "error":
            raise DownloadError(self.translate("The download of the trailer « {title} » failed.", title=title))

    def match_filter(self, info, *, incomplete):
        """
        Check the duration of a video and raise an error if it exceeds the maximum length.

        :param info: Information dictionary of the video
        :param max_length: Maximum allowed length in seconds
        """
        duration = info.get("duration")
        max_length = self.config.get("YT_DLP_MAX_LENGTH", None)
        if max_length is None:
            max_length = duration
            self.logger.warning("YT_DLP_MAX_LENGTH is not defined. All trailers will be uploaded regardless of their length.")

        if duration and (int(duration) > int(max_length)):
            title = info.get("title")
            raise DurationError(
                self.translate(
                    "Trailer « {title} » is greater than « {duration} ».",
                    title=title,
                    duration=f"{duration}/{max_length}",
                )
            )

    def yt_dlp_process(self, link: dict, ytdl_opts: dict) -> None:
        """
        Download trailer using yt-dlp.

        :param link: Trailer link information
        :param ytdl_opts: Options for yt-dlp
        """
        ydl = yt_dlp.YoutubeDL(ytdl_opts)

        title = link.get("name")
        yt_link = link.get("yt_link")

        # Log the process of downloading the trailer using yt-dlp
        self.logger.info("Trailer download from « {link} » for « {title} ».", title=f"{title}", link=yt_link)
        ydl.download(yt_link)

    def download_trailers(self, links: list, item: dict) -> str:
        """
        Download trailers from YouTube.

        :param links: List of YouTube trailer links
        :param item: Metadata of the item (movie or TV show)
        :return: Path to the cache directory where trailers are downloaded
        """

        title = item["use_title"]
        cache_path = f"tmp/{item['tmp']}"
        os.makedirs(cache_path, exist_ok=True)

        ytdl_opts = {
            "progress_hooks": [self.progress_hooks],
            "format": self.config.get("YT_DLP_FORMAT", "bestvideo+bestaudio"),
            "noplaylist": True,
            "no_warnings": self.config.get("YT_DLP_NO_WARNINGS", False),
            "ignoreerrors": True,
            "quiet": self.config.get("APP_QUIET_MODE", False),
            "noprogress": self.config.get("APP_QUIET_MODE", False),
            "sleep_interval_requests": self.config.get("YT_DLP_INTERVAL_REQUESTS", 1),
            "match_filter": self.match_filter,
        }
        if self.config.get("YT_DLP_SKIP_INTROS", False):
            ytdl_opts["postprocessors"] = [
                {"key": "SponsorBlock"},
                {"key": "ModifyChapters", "remove_sponsor_segments": self.config.get("YT_DLP_SPONSORS_BLOCK", [])},
            ]
        # Loop through each trailer link and attempt to download it

        for link in links:
            # if only one trailer use default name
            if self.config.get("APP_ONLY_ONE_TRAILER", True):
                # if have trailer continue to another item
                if len(os.listdir(cache_path)) == 1:
                    continue
                ytdl_opts["outtmpl"] = f"{cache_path}/{title}.%(ext)s"
            else:
                ytdl_opts["outtmpl"] = f"{cache_path}/{link['name']}"

            self.logger.info("Search trailers with « {query} ».", query=link["query_type"])
            try:
                ydl = yt_dlp.YoutubeDL(ytdl_opts)
                self.logger.info("Trailer download from « {link} » for « {title} ».", title=f"{title}", link=link.get("yt_link"))
                ydl.download(link.get("yt_link"))
                if len(os.listdir(cache_path)) == 0:
                    self.logger.warning("No trailers were found with « {query} ».", query=link["query_type"])
            except DownloadError as e:
                self.logger.error("Unexpected error for {link}: {error}", link=f"{title} - {link}", error=str(e))
                continue
        return cache_path
