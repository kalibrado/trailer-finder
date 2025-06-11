"""
Module for interacting with radarr API to find and download trailers for movie.

This module connects to radarr using its API to retrieve movie information and search for trailers
associated with each series. It uses configurations provided in `config.yaml` to customize paths, API keys,
and other settings.

Dependencies:
    - os: Operating system interface for file operations.
    - pyarr: Library for interfacing with radarr API.
    - modules.utils: Utility functions for handling trailers, downloading from YouTube, and post-processing with FFMPEG.
    - modules.logger.Logger: Logger instance for logging messages.

Functions:
    - radarr(logger, config, utils):
        Main function to find and download trailers for movies using the Radarr API.

    - Args:
        logger (Logger): Logger instance for logging messages.
        config (dict): Configuration dictionary containing settings from `config.yaml`.
        utils (Utils): Utility functions instance for handling trailer downloads and processing.

Usage:
    This module is intended to be executed as a standalone script to find and download trailers for movie
    managed by radarr. It uses configurations from `config.yaml` to customize behavior such as file paths,
    API keys, and search parameters. Ensure `config.yaml` is correctly configured before running the script.
"""

import os
from pyarr import RadarrAPI  # type: ignore
from modules.logger import Logger
from modules.utils import Utils
from modules.decorators import exception_logger


@exception_logger(Logger)
def radarr(logger: Logger, config: dict, utils: Utils) -> None:
    """
    Main function to find and download trailers for movies using the Radarr API.

    :param logger: Logger instance for logging messages
    :param config: Configuration dictionary containing Radarr API host and other settings
    :param utils: Utility functions instance for various helper functions
    """
    host = config.get("RADARR_HOST", None)
    api = config.get("RADARR_API", None)

    if host is None or api is None:
        logger.warning("app_not_configured", app="Radarr")
        return

    # Initialize Radarr API
    radarr_api = RadarrAPI(host, api)

    print("--------------------------------")
    logger.info("movie_finder_start")

    # Iterate through all movies in Radarr
    for movie in radarr_api.get_movie():
        assert isinstance(movie, dict)

        path = movie.get("path", None)
        title = utils.get_title(movie)
        # defined title to use for all process
        movie["use_title"] = title
        year = movie.get("year", None)
        movie["tmp"] = f"{title} ({year})"

        if path is None or title is None:
            continue

        movie["trailers_dest"] = os.path.join(movie["path"], config["APP_DEFAULT_DIR"])

        custom_path = config.get("APP_CUSTOM_PATH", None)
        custom_name = config.get("APP_CUSTOM_NAME_MOVIE", None)

        if custom_path and custom_name:
            movie["trailers_dest"] = os.path.join(custom_path, custom_name, title)

        # create ooutputs folder if not exist
        os.makedirs(movie["trailers_dest"], exist_ok=True)

        utils.check_space(movie["trailers_dest"])

        print("--------------------------------")

        # outputs list dir
        trailers_in_outputs_folder = os.listdir(movie["trailers_dest"])

        # count trailers in ouputs
        count = len(trailers_in_outputs_folder)

        # Skip if trailer already exists
        if config["APP_ONLY_ONE_TRAILER"] and count >= 1:
            logger.success("already_have", title=title, year=year, count=count)
            continue

        logger.info("search_trailers", title=title, year=year)

        # Fetch trailers using TMDB ID
        trailers = utils.trailer_pull(movie["tmdbId"], "movie", movie)
        list_of_trailers = utils.get_new_trailers(trailers, trailers_in_outputs_folder)
        utils.download_trailers(list_of_trailers, movie)

    logger.info("movie_finder_end")
    print("--------------------------------")
