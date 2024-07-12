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

    if config["sonarr_host"] is None or config["sonarr_api"] is None:
        return

    # Initialize Sonarr API
    sonarr_api = SonarrAPI(config["sonarr_host"], config["sonarr_api"])

    logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
    logger.info("[ SONARR ]", "Show trailer finder started.")

    # Iterate through all TV series in Sonarr
    for show in sonarr_api.get_series():
        # Path to store trailers
        show["outputs_folder"] = os.path.join(show["path"], config["dir_backdrops"])

        # create folder in custom path using name cache folder
        if config["custom_path"]:
            show["outputs_folder"] = os.path.join(
                config["custom_path"], config["custom_name_tv_show"], show["title"]
            )

        # create ooutputs folder if not exist
        os.makedirs(show["outputs_folder"], exist_ok=True)

        if not utils.check_space(show["outputs_folder"]):  # Skip if not enough space
            continue

        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
        trailer_count = len(os.listdir(show["outputs_folder"]))

        # Skip if trailer already exists
        if config["only_one_trailer"] and trailer_count >= 1:
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
        tv_show_pack = utils.trailer_pull(show["imdbId"], "tv", parent_mode=True)
        # No trailers found
        if len(tv_show_pack) == 0:
            logger.warning(
                "\t\t ->",
                "No trailer is available for {title} ({year})",
                title=show["title"],
                year=show["year"],
            )
            continue

        # Download trailers for each episode
        for season in tv_show_pack:
            season_trailers = utils.trailer_pull(season["id"], "tv")
            # No trailers found for episode
            # fix :add here youtube search keyword
            if len(season_trailers) == 0:
                logger.warning(
                    "\t\t ->",
                    "No trailer is available for {title} ({year})",
                    title=show["title"],
                    year=show["year"],
                )
                continue

            utils.trailer_download(season_trailers, show)

    logger.info("[ SONARR ]", "Show trailer finder ended.")
    logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
