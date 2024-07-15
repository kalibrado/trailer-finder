"""
modules/sonarr.py

This module interacts with Sonarr API to find and download trailers for TV series.
"""

import os
from pyarr import SonarrAPI
from modules.utils import Utils


def sonarr(logger, config: dict, utils: Utils):
    """
    Main function to find and download trailers for TV series using Sonarr API.
    """

    host = config.get("sonarr_host", None)
    api = config.get("sonarr_api", None)

    if host is None or api is None:
        logger.warning(
            "[ SONARR ]",
            "Warning: {Warning}",
            Warning=" the sonarr application is not configured in the yaml file ",
        )
        return
    try:
        # Initialize Sonarr API
        sonarr_api = SonarrAPI(host, api)

        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
        logger.info("[ SONARR ]", "Show trailer finder started.")

        # Iterate through all TV series in Sonarr
        for show in sonarr_api.get_series():
            assert isinstance(show, dict)

            path = show.get("path", None)
            title = show.get("title", None)
            year = show.get("year", None)

            if path is None or title is None:
                # sonarr item dont have path or title
                continue

            # Path to store trailers
            show["outputs_folder"] = os.path.join(path, config["dir_backdrops"])

            custom_path = config.get("custom_path", None)
            custom_name_tv_show = config.get("custom_name_tv_show", None)
            # create folder in custom path using name cache folder
            if custom_path and custom_name_tv_show:
                show["outputs_folder"] = os.path.join(
                    custom_path, custom_name_tv_show, title
                )

            outputs_folder = show["outputs_folder"]
            # create ooutputs folder if not exist
            os.makedirs(outputs_folder, exist_ok=True)

            # Skip if not enough space
            if not utils.check_space(outputs_folder):
                continue

            logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
            # count trailers in ouputs
            count = len(os.listdir(outputs_folder))

            # Skip if trailer already exists
            if config["only_one_trailer"] and count >= 1:
                logger.success(
                    "\t ->",
                    "{title} ({year}) already has {count} trailers.",
                    title=title,
                    year=year,
                    count=count,
                )
                continue

            logger.info(
                "\t -> SCAN",
                "Looking for {title} ({year}) trailers",
                title=title,
                year=year,
            )

            # Fetch trailers using IMDb ID
            tv_show_pack = utils.trailer_pull(show["imdbId"], "tv", parent_mode=True)
            # No trailers found
            if len(tv_show_pack) == 0:
                logger.warning(
                    "\t ->",
                    "No trailer is available for {title} ({year})",
                    title=title,
                    year=year,
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
                        title=title,
                        year=year,
                    )
                    continue

                utils.trailer_download(season_trailers, show)

        logger.info("[ SONARR ]", "Show trailer finder ended.")
        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
    except Exception as err:
        logger.error("[ SONARR ]", "An error occurred: {error}", error=err)
