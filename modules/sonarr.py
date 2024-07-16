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

    host = config.get("SONARR_HOST", None)
    api = config.get("SONARR_API", None)

    if host is None or api is None:
        logger.warning("[ SONARR ]", "Warning: {warning}", Warning=" the sonarr application is not configured in the yaml file ")
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
            title = utils.get_title(show)
            # defined title to use for all process
            show["use_title"] = title
            year = show.get("year", None)
            show["tmp"] = f"{title} ({year})"

            if path is None or title is None:
                continue

            custom_path = config.get("APP_CUSTOM_PATH", None)
            custom_name = config.get("APP_CUSTOM_NAME_SHOW", None)
            # create folder in custom path using name cache folder
            if custom_path and custom_name:
                show["outputs_folder"] = os.path.join(custom_path, custom_name, title)

            outputs_folder = show["outputs_folder"]
            # create outputs folder if not exist
            os.makedirs(outputs_folder, exist_ok=True)

            # Skip if not enough space
            if not utils.check_space(outputs_folder):
                continue

            logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")

            seasons = show.get("seasons", [])
            if len(seasons) > 0:
                for season in seasons:
                    title_format = config.get("YT_DLP_SEARCH_KEYWORD_SEASON", "{show} Season {season_number}")
                    show["use_title"] = title_format.format(show=title, season_number=season["seasonNumber"])
                    # Path to store trailers
                    show["outputs_folder"] = os.path.join(outputs_folder, show["use_title"])
                    os.makedirs(show["outputs_folder"], exist_ok=True)
                    # outputs list dir
                    trailers_in_outputs_folder = os.listdir(show["outputs_folder"])
                    count = len(trailers_in_outputs_folder)

                    if config["APP_ONLY_ONE_TRAILER"] and count >= 1:
                        logger.success("\t ->", "{title} ({year}) already has {count} trailers.", title=show["use_title"], year=year, count=count)
                        continue
                    logger.info("\t ->", "Looking for {title} ({year}) trailers", title=show["use_title"], year=year)
                    show["query_type"] = "TMDB API"
                    season_trailers = utils.trailer_pull(show["tmdbId"], "tv", seasonNumber=season["seasonNumber"])
                    list_of_trailers = utils.get_new_trailers(season_trailers, trailers_in_outputs_folder)

                    # No trailers found
                    if len(list_of_trailers) == 0:
                        logger.warning("\t\t ->", "No trailers available on {query}", query=show["query_type"])
                        link = {
                            "name": show["use_title"],
                            "yt_link": f"gvsearch5:{show["use_title"]} {config.get('YT_DLP_SEARCH_KEYWORD')}",
                        }
                        list_of_trailers = [link]
                        logger.info("\t\t  ->", "Search trailer with {query}", query=link["yt_link"])
                        show["query_type"] = link["yt_link"]

                    utils.download_trailers(list_of_trailers, show)

        logger.info("[ SONARR ]", "Show trailer finder ended.")
        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
    except Exception as err:
        logger.error("[ SONARR ]", "An error occurred: {error}", error=err)
