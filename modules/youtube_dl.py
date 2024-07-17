"""
Module for handling YouTube trailer downloads using yt-dlp.

This module defines the YoutubeDL class that utilizes yt-dlp to download trailers from YouTube
based on provided links and configuration options.

Classes:
    YoutubeDL: Class for downloading trailers using yt-dlp.

Usage Example:

    # Importing the YoutubeDL class
    from modules.youtube_dl import YoutubeDL

    # Initialize a logger instance (assuming 'logger' is already initialized)
    logger = Logger()

    # Example configuration dictionary
    config = {
        "YT_DLP_MAX_LENGTH": 600,  # Maximum allowed duration for trailers in seconds
        "YT_DLP_FORMAT": "bestvideo+bestaudio",  # Preferred format for downloading
        "YT_DLP_NO_WARNINGS": False,  # Disable yt-dlp warnings
        "APP_QUIET_MODE": True,  # Enable quiet mode
        "YT_DLP_INTERVAL_RESQUESTS": 2,  # Interval for sleep between requests
        "APP_ONLY_ONE_TRAILER": True,  # Download only one trailer per item
    }

    # Initialize the YoutubeDL instance
    youtube_dl = YoutubeDL(logger, config)

    # Example item metadata
    item = {
        "use_title": "MovieTitle",  # Title of the movie
    }

    # Example trailer links (assuming 'links' is a list of dictionaries with 'name' and 'yt_link')
    links = [
        {"name": "Trailer1", "yt_link": "https://www.youtube.com/watch?v=video1"},
        {"name": "Trailer2", "yt_link": "https://www.youtube.com/watch?v=video2"},
    ]

    # Download trailers using YoutubeDL
    cache_path = youtube_dl.download_trailers(links, item)

    # Process the downloaded trailers (example)
    # Note: Implement post-processing or further handling as per your application needs

"""

import os
import yt_dlp
from modules.logger import Logger
from modules.exceptions import DurationError, DonwloadError
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
            raise DonwloadError(self.translate("The download of the trailer « {title} » failed.", title=title))

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
            raise DurationError(self.translate("Trailer « {title} » is greater than « {duration} ».", title=title, duration=duration))

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
            "sleep_interval_requests": self.config.get("YT_DLP_INTERVAL_RESQUESTS", 1),
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
            try:
                ydl = yt_dlp.YoutubeDL(ytdl_opts)
                self.logger.info("Trailer download from « {link} » for « {title} ».", title=f"{title}", link=link.get("yt_link"))
                ydl.download(link.get("yt_link"))
            except DonwloadError as e:
                self.logger.error("Unexpected error for {link}: {error}", link=f"{title} - {link}", error=str(e))
                continue
        return cache_path
