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
from pyarr import SonarrAPI # type: ignore
from modules.utils import Utils
from modules.logger import Logger


def sonarr(logger: Logger, config: dict, utils: Utils):
    """
    Main function to find and download trailers for TV series using Sonarr API.
    """

    host = config.get("SONARR_HOST", None)
    api = config.get("SONARR_API", None)

    if host is None or api is None:
        logger.warning("app_not_configured", app="Sonarr")
        return

    # Initialize Sonarr API
    sonarr_api = SonarrAPI(host, api)
    print("--------------------------------")
    logger.info("tvshow_finder_start")

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
            continue

        show["trailers_dest"] = os.path.join(show["path"], config["APP_DEFAULT_DIR"])

        custom_path = config.get("APP_CUSTOM_PATH", None)
        custom_name = config.get("APP_CUSTOM_NAME_SHOW", None)
        # create folder in custom path using name cache folder
        if custom_path and custom_name:
            show["trailers_dest"] = os.path.join(custom_path, custom_name, title)

        # create outputs folder if not exist
        os.makedirs(show["trailers_dest"], exist_ok=True)

        utils.check_space(show["trailers_dest"])


        print("--------------------------------")

        seasons = show.get("seasons", [])
        if len(seasons) > 0:
            for season in seasons:
                title_format = config.get(
                    "YT_DLP_SEARCH_KEYWORD_SEASON", "{show} Season {season_number}"
                )
                show["use_title"] = title_format.format(
                    show=title, season_number=season["seasonNumber"]
                )
                show["trailers_dest"] = os.path.join(
                    show["trailers_dest"], show["use_title"]
                )

                os.makedirs(show["outputs_folder"], exist_ok=True)

                utils.check_space(show["outputs_folder"])


                trailers_in_outputs_folder = os.listdir(show["outputs_folder"])
                count = len(trailers_in_outputs_folder)

                if config["APP_ONLY_ONE_TRAILER"] and count >= 1:
                    logger.success("already_have", title=show["use_title"], count=count)
                    continue

                logger.info("search_trailers", title=show["use_title"])
                season_trailers = utils.trailer_pull(
                    show["tmdbId"], "tv", show, seasonNumber=season["seasonNumber"]
                )
                list_of_trailers = utils.get_new_trailers(
                    season_trailers, trailers_in_outputs_folder
                )
                utils.download_trailers(list_of_trailers, show)
                print("--------------------------------")

    logger.info("tvshow_finder_end")
    print("--------------------------------")
