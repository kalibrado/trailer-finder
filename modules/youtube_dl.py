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


class YoutubeDL:
    def __init__(self, logger: Logger, config: dict) -> None:
        """
        Initialize YoutubeDL class with a logger and configuration.

        :param logger: Logger instance for logging messages
        :param config: Configuration dictionary or list
        """
        self.logger = logger
        self.config = config

    def dl_progress(self, d):
        # Define a download progress function to handle yt-dlp progress hooks
        if d["status"] == "finished":
            self.logger.success("\t\t ->", "Trailer {filename} downloaded.", filename=d["filename"].split('/')[-1])
        if d["status"] == "error":
            raise ValueError("Trailer {filename} download failed.", filename=d["filename"])

    def check_duration(self, info, *, incomplete):
        """
        Check the duration of a video and raise an error if it exceeds the maximum length.

        :param info: Information dictionary of the video
        :param max_length: Maximum allowed length in seconds
        """
        duration = info.get("duration")
        max_length = self.config.get("YT_DLP_MAX_LENGTH", None)
        if max_length is None:
            return
        if duration and (int(duration) > int(max_length)):
            raise ValueError("Invalid duration: {duration}s".format(duration=duration))

    def yt_dlp_process(self, link: dict, ytdl_opts: dict) -> None:
        """
        Download trailer using yt-dlp.

        :param link: Trailer link information
        :param ytdl_opts: Options for yt-dlp
        """
        ydl = yt_dlp.YoutubeDL(ytdl_opts)

        title = link.get("name")
        yt_link = link.get("yt_link")

        try:
            # Log the process of downloading the trailer using yt-dlp
            self.logger.info("\t\t ->", "Downloading {title} trailer from {link}", title=f"{title}", link=yt_link)
            ydl.download(yt_link)

        except yt_dlp.DownloadError as e:
            # Handle download errors during yt-dlp download and log them
            self.logger.error("\t\t ->", "Download error for {link}: {error}", link=f"{title} - {yt_link}", error=str(e))
        except Exception as e:
            # Handle unexpected errors during yt-dlp download and log them
            self.logger.error("\t\t ->", "Unexpected error for {link}: {error}", link=f"{title} - {yt_link}", error=str(e))

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
            "progress_hooks": [self.dl_progress],
            "format": self.config.get("YT_DLP_FORMAT", "bestvideo+bestaudio"),
            "noplaylist": True,
            "no_warnings": self.config.get("YT_DLP_NO_WARNINGS", False),
            "ignoreerrors": True,
            "quiet": self.config.get("APP_QUIET_MODE", False),
            "noprogress": self.config.get("APP_QUIET_MODE", False),
            "sleep_interval_requests": self.config.get("YT_DLP_INTERVAL_RESQUESTS", 1),
            "match_filter": self.check_duration,
        }
        if self.config.get("YT_DLP_SKIP_INTROS", False):
            ytdl_opts["postprocessors"] = [
                {"key": "SponsorBlock"},
                {"key": "ModifyChapters", "remove_sponsor_segments": self.config.get("YT_DLP_SPONSORS_BLOCK", [])},
            ]
        # Loop through each trailer link and attempt to download it
        for link in links:
            if link:
                try:
                    # if only one trailer use default name
                    if self.config.get("APP_ONLY_ONE_TRAILER", True):
                        # if have trailer continue to another item
                        if len(os.listdir(cache_path)) == 1:
                            continue
                        ytdl_opts["outtmpl"] = f"{cache_path}/{title}.%(ext)s"
                    else:
                        ytdl_opts["outtmpl"] = f"{cache_path}/{link['name']}"

                    self.yt_dlp_process(link, ytdl_opts)
                except Exception as e:
                    self.logger.error("\t\t ->", "Unexpected error during download for {link}: {error}", link=link["name"], error=str(e))

        return cache_path
