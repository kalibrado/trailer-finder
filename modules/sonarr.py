"""
modules/sonarr.py

This module interacts with Sonarr API to find and download trailers for TV series.
"""

import os
from pyarr import SonarrAPI
from modules.utils import Utils


def sonarr(logger, config, utils: Utils):
    """
    Main function to find and download trailers for TV series using Sonarr API.
    """
    sonarr_api = SonarrAPI(config["sonarr_host"], config["sonarr_api"])  # Initialize Sonarr API
    logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
    logger.info("[ SONARR ]", "Show trailer finder started.")

    # Iterate through all TV series in Sonarr
    for show in sonarr_api.get_series():
        dir_backdrops = os.path.join(
            show["path"], config["dir_backdrops"]
        )  # Path to store trailers

        if not os.path.exists(dir_backdrops):  # Skip if directory doesn't exist
            continue

        if show["statistics"]["sizeOnDisk"] == 0:  # Skip if show is not downloaded
            continue

        if not utils.check_space(show["path"]):  # Skip if not enough space
            continue

        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
        trailer_count = len(os.listdir(dir_backdrops))

        if (
            config["only_one_trailer"] and trailer_count >= 1
        ):  # Skip if trailer already exists
            logger.success(
                "\t\t ->",
                "{title} ({year}) already has {count} trailers.",
                title=show["title"],
                year=show["year"],
                count=trailer_count,
            )
            continue

        logger.info(
            "\t -> SCAN",
            "Looking for {title} ({year}) trailers",
            title=show["title"],
            year=show["year"],
        )

        # Fetch trailers using IMDb ID
        episodes = utils.trailer_pull(show["imdbId"], "tv", parent_mode=True)
        if len(episodes) == 0:  # No trailers found
            logger.warning(
                "\t\t ->",
                "No trailer is available for {title} ({year})",
                title=show["title"],
                year=show["year"],
            )
            continue

        # Download trailers for each episode
        for episode in episodes:
            episode_trailers = utils.trailer_pull(episode["id"], "tv")
            if len(episode_trailers) == 0:  # No trailers found for episode
                logger.warning(
                    "\t\t ->",
                    "No trailer is available for {title} ({year})",
                    title=show["title"],
                    year=show["year"],
                )
                continue

            utils.trailer_download(episode_trailers, show)

    logger.info("[ SONARR ]", "Show trailer finder ended.")
    logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
