"""
modules/radarr.py

This module interacts with the Radarr API to find and download trailers for movies.

Classes:
    None

Functions:
    - radarr(logger: Logger, config: dict, utils: Utils) -> None:
        Main function to find and download trailers for movies using the Radarr API.

    - Args:
        logger (Logger): Logger instance for logging messages.
        config (dict): Configuration dictionary containing settings from `config.yaml`.
        utils (Utils): Utility functions instance for handling trailer downloads and processing.

"""

import os
from pyarr import RadarrAPI
from modules.logger import Logger
from modules.utils import Utils
from modules.exceptions import InsufficientDiskSpaceError


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
        logger.warning("{app} not configured.", app="Radarr")
        return

    try:
        # Initialize Radarr API
        radarr_api = RadarrAPI(host, api)

        print("--------------------------------")
        logger.info("Movie trailers finder started.")

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
                # radarr item dont have path or title
                logger.error("Warning « {warning} ».", warning=f"Path or Title not exist in: {movie}")
                continue

            movie["trailers_dest"] = os.path.join(movie["path"], config["APP_DEFAULT_DIR"])

            custom_path = config.get("APP_CUSTOM_PATH", None)
            custom_name = config.get("APP_CUSTOM_NAME_MOVIE", None)

            if custom_path and custom_name:
                movie["trailers_dest"] = os.path.join(custom_path, custom_name, title)

            # create ooutputs folder if not exist
            os.makedirs(movie["trailers_dest"], exist_ok=True)

            try:
                # Skip if not enough space
                utils.check_space(movie["trailers_dest"])
            except InsufficientDiskSpaceError as err:
                logger.error("An error has occurred « {error} ».", error=err)
                continue

            print("--------------------------------")

            # outputs list dir
            trailers_in_outputs_folder = os.listdir(movie["trailers_dest"])

            # count trailers in ouputs
            count = len(trailers_in_outputs_folder)

            # Skip if trailer already exists
            if config["APP_ONLY_ONE_TRAILER"] and count >= 1:
                logger.success("« {title} » already has « {count} » trailers.", title=title, year=year, count=count)
                continue

            logger.info("Search trailers for « {title} ».", title=title, year=year)

            # Fetch trailers using TMDB ID
            trailers = utils.trailer_pull(movie["tmdbId"], "movie", movie)
            list_of_trailers = utils.get_new_trailers(trailers, trailers_in_outputs_folder)
            utils.download_trailers(list_of_trailers, movie)

        logger.info("Movie trailers finder ended.")
        print("--------------------------------")
    except AssertionError as err:
        logger.error("An error has occurred « {error} ».", error={"error": err, "host": host})
