"""
modules/radarr.py

This module interacts with the Radarr API to find and download trailers for movies.
"""

import os
from pyarr import RadarrAPI
from modules.logger import Logger
from modules.utils import Utils


def radarr(logger: Logger, config: list, utils: Utils):
    """
    Main function to find and download trailers for movies using the Radarr API.
    """

    if config["radarr_host"] is None or config["radarr_api"] is None:
        return

    # Initialize Radarr API
    radarr_api = RadarrAPI(config["radarr_host"], config["radarr_api"])

    logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
    logger.info("[ RADARR ]", "Movie trailer finder started.")

    # Iterate through all movies in Radarr
    for movie in radarr_api.get_movie():
        movie["outputs_folder"] = os.path.join(movie["path"], config["dir_backdrops"])

        # create folder in custom path using name cache folder
        if config["custom_path"]:
            movie["outputs_folder"] = os.path.join(
                config["custom_path"], config["custom_name_movie"], movie["title"]
            )

        # create ooutputs folder if not exist
        os.makedirs(movie["outputs_folder"], exist_ok=True)

        if not utils.check_space(movie["outputs_folder"]):  # Skip if not enough space
            continue

        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
        trailer_count = len(os.listdir(movie["outputs_folder"]))
        if (
            config["only_one_trailer"] and trailer_count >= 1
        ):  # Skip if trailer already exists
            logger.success(
                "\t ->",
                "{title} ({year}) already has {count} trailers.",
                title=movie["title"],
                year=movie["year"],
                count=trailer_count,
            )
            continue

        logger.info(
            "\t -> SCAN",
            "Looking for {title} ({year}) trailers",
            title=movie["title"],
            year=movie["year"],
        )

        # Fetch trailers using TMDB ID
        trailers = utils.trailer_pull(movie["tmdbId"], "movie")
        # No trailers found
        # fix :add here youtube search keyword
        if len(trailers) == 0:
            logger.warning(
                "\t ->",
                "No trailer is available for {title} ({year})",
                title=movie["title"],
                year=movie["year"],
            )
            continue

        list_of_trailers = utils.check_existing_trailer(
            trailers, os.listdir(movie["outputs_folder"])
        )

        utils.trailer_download(list_of_trailers, movie)

    logger.info("[ RADARR ]", "Movie trailer finder ended.")
    logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
