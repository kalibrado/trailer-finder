"""
Module for interacting with Sonarr API to find and download trailers for TV series.

This module connects to Sonarr using its API to retrieve TV series information and search for trailers
associated with each series. It uses configurations provided in `config.yaml` to customize paths, API keys,
and other settings.

Dependencies:
    - os: Operating system interface for file operations.
    - pyarr: Library for interfacing with Sonarr API.
    - modules.utils: Utility functions for handling trailers, downloading from YouTube, and post-processing with FFMPEG.
    - modules.logger.Logger: Logger instance for logging messages.
    - modules.exceptions.InsufficientDiskSpaceError: Exception raised when there is insufficient disk space for operations.

Functions:
    - sonarr(logger, config, utils):
        Main function to find and download trailers for TV series using Sonarr API.

    - Args:
        logger (Logger): Logger instance for logging messages.
        config (dict): Configuration dictionary containing settings from `config.yaml`.
        utils (Utils): Utility functions instance for handling trailer downloads and processing.

Usage:
    This module is intended to be executed as a standalone script to find and download trailers for TV series
    managed by Sonarr. It uses configurations from `config.yaml` to customize behavior such as file paths,
    API keys, and search parameters. Ensure `config.yaml` is correctly configured before running the script.
"""

import os
from pyarr import SonarrAPI
from modules.utils import Utils
from modules.logger import Logger
from modules.exceptions import InsufficientDiskSpaceError


def sonarr(logger: Logger, config: dict, utils: Utils):
    """
    Main function to find and download trailers for TV series using Sonarr API.
    """

    host = config.get("SONARR_HOST", None)
    api = config.get("SONARR_API", None)

    if host is None or api is None:
        logger.warning("{app} not configured.", app="Sonarr")
        return

    try:
        # Initialize Sonarr API
        sonarr_api = SonarrAPI(host, api)
        print("--------------------------------")
        logger.info("TV Show trailers finders started.")

        # Iterate through all TV series in Sonarr
        for show in sonarr_api.get_series():
            assert isinstance(show, dict)

            path = show.get("path", None)
            title = utils.get_title(show)
            # defined title to use for all process
            show["use_title"] = title
            year = show.get("year", None)
            # for tmp folder name
            show["tmp"] = f"{title} ({year})"

            if path is None or title is None:
                # radarr item dont have path or title
                logger.warning("Warning « {warning} ».", warning=show)
                continue

            show["trailers_dest"] = os.path.join(show["path"], config["APP_DEFAULT_DIR"])

            custom_path = config.get("APP_CUSTOM_PATH", None)
            custom_name = config.get("APP_CUSTOM_NAME_SHOW", None)
            # create folder in custom path using name cache folder
            if custom_path and custom_name:
                show["trailers_dest"] = os.path.join(custom_path, custom_name, title)

            # create outputs folder if not exist
            os.makedirs(show["trailers_dest"], exist_ok=True)

            try:
                # Skip if not enough space
                utils.check_space(show["trailers_dest"])
            except InsufficientDiskSpaceError as err:
                logger.error("An error has occurred « {error} ».", error=err)
                continue

            print("--------------------------------")

            seasons = show.get("seasons", [])
            if len(seasons) > 0:
                for season in seasons:
                    title_format = config.get("YT_DLP_SEARCH_KEYWORD_SEASON", "{show} Season {season_number}")
                    show["use_title"] = title_format.format(show=title, season_number=season["seasonNumber"])
                    show["trailers_dest"] = os.path.join(show["trailers_dest"], show["use_title"])

                    os.makedirs(show["trailers_dest"], exist_ok=True)

                    trailers_in_outputs_folder = os.listdir(show["trailers_dest"])
                    count = len(trailers_in_outputs_folder)

                    if config["APP_ONLY_ONE_TRAILER"] and count >= 1:
                        logger.success("« {title} » already has « {count} » trailers.", title=show["use_title"], count=count)
                        continue

                    logger.info("Search trailers for « {title} ».", title=show["use_title"])
                    season_trailers = utils.trailer_pull(show["tmdbId"], "tv", show, seasonNumber=season["seasonNumber"])
                    list_of_trailers = utils.get_new_trailers(season_trailers, trailers_in_outputs_folder)
                    utils.download_trailers(list_of_trailers, show)
                    print("--------------------------------")

        logger.info("TV Show trailers finder ended.")
        print("--------------------------------")
    except Exception as err:
        debug = {"error": err, "host": host}
        logger.error("An error has occurred « {error} ».", error=debug)
