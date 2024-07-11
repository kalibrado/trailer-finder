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
    radarr_api = RadarrAPI(
        config["radarr_host"], config["radarr_api"]
    )  # Initialize Radarr API
    logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
    logger.info("[ RADARR ]", "Movie trailer finder started.")

    # Iterate through all movies in Radarr
    for movie in radarr_api.get_movie():
        dir_backdrops = os.path.join(
            movie["path"], config["dir_backdrops"]
        )  # Path to store trailers
        if not os.path.exists(dir_backdrops):  # Skip if directory doesn't exist
            continue
        if movie["sizeOnDisk"] == 0:  # Skip if movie is not downloaded
            continue
        if not utils.check_space(movie["path"]):  # Skip if not enough space
            continue

        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
        trailer_count = len(os.listdir(dir_backdrops))
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
        if len(trailers) == 0:  # No trailers found
            logger.warning(
                "\t ->",
                "No trailer is available for {title} ({year})",
                title=movie["title"],
                year=movie["year"],
            )
            continue

        # Download trailers
        utils.trailer_download(
            utils.check_existing_trailer(trailers, os.listdir(dir_backdrops)),
            movie,
        )

    logger.info("[ RADARR ]", "Movie trailer finder ended.")
    logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
