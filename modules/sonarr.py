"""
modules/sonarr.py

This module interacts with Sonarr API to find and download trailers for TV series.
"""

import os
from pyarr import SonarrAPI
from modules.utils import Utils
from modules.exceptions import InsufficientDiskSpaceError


def sonarr(logger, config: dict, utils: Utils):
    """
    Main function to find and download trailers for TV series using Sonarr API.
    """

    host = config.get("SONARR_HOST", None)
    api = config.get("SONARR_API", None)

    if host is None or api is None:
        logger.warning("Warning « {warning} ».", Warning=" the sonarr application is not configured in the yaml file ")
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
            show["tmp"] = f"{title} ({year})"

            if path is None or title is None:
                # radarr item dont have path or title
                logger.error("Warning « {warning} ».", warning=f"Path or Title not exist in: {show}")
                continue

            show["outputs_folder"] = os.path.join(show["path"], config["APP_DEFAULT_DIR"])

            custom_path = config.get("APP_CUSTOM_PATH", None)
            custom_name = config.get("APP_CUSTOM_NAME_SHOW", None)
            # create folder in custom path using name cache folder
            if custom_path and custom_name:
                show["outputs_folder"] = os.path.join(custom_path, custom_name, title)

            # create outputs folder if not exist
            os.makedirs(show["outputs_folder"], exist_ok=True)

            try:
                # Skip if not enough space
                utils.check_space(show["outputs_folder"])
            except InsufficientDiskSpaceError as err:
                logger.error("An error has occurred: {error}.", error=err)
                continue

            print("--------------------------------")

            seasons = show.get("seasons", [])
            if len(seasons) > 0:
                for season in seasons:
                    title_format = config.get("YT_DLP_SEARCH_KEYWORD_SEASON", "{show} Season {season_number}")
                    show["use_title"] = title_format.format(show=title, season_number=season["seasonNumber"])
                    show["outputs_folder"] = os.path.join(show["outputs_folder"], show["use_title"])

                    os.makedirs(show["outputs_folder"], exist_ok=True)
                    try:
                        # Skip if not enough space
                        utils.check_space(show["outputs_folder"])
                    except InsufficientDiskSpaceError as err:
                        logger.error("An error has occurred: {error}.", error=err)
                        continue
                    trailers_in_outputs_folder = os.listdir(show["outputs_folder"])
                    count = len(trailers_in_outputs_folder)

                    if config["APP_ONLY_ONE_TRAILER"] and count >= 1:
                        logger.success("« {title} » already has « {count} » trailers.", title=show["use_title"], year=year, count=count)
                        continue

                    logger.info("Search trailers for « {title} ».", title=show["use_title"], year=year)
                    show["query_type"] = "TMDB API"
                    season_trailers = utils.trailer_pull(show["tmdbId"], "tv", seasonNumber=season["seasonNumber"])
                    list_of_trailers = utils.get_new_trailers(season_trailers, trailers_in_outputs_folder)

                    # No trailers found
                    if len(list_of_trailers) == 0:
                        logger.warning("No trailers were found with « {query} ».", query=show["query_type"])
                        link = {
                            "name": show["use_title"],
                            "yt_link": f"gvsearch5:{show['use_title']} {config.get('YT_DLP_SEARCH_KEYWORD')}",
                        }
                        list_of_trailers = [link]
                        logger.info("Search trailers with « {query} ».", query=link["yt_link"])
                        show["query_type"] = link["yt_link"]
                    utils.download_trailers(list_of_trailers, show)

        logger.info("TV Show trailers finder ended.")
        print("--------------------------------")
    except Exception as err:
        debug = {"error": err, "host": host}
        logger.error("An error has occurred: {error}.", error=debug)
