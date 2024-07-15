"""
modules/radarr.py

This module interacts with the Radarr API to find and download trailers for movies.
"""

import os
from pyarr import RadarrAPI
from modules.logger import Logger
from modules.utils import Utils


def radarr(logger: Logger, config: dict, utils: Utils):
    """
    Main function to find and download trailers for movies using the Radarr API.
    """

    host = config.get("radarr_host", None)
    api = config.get("radarr_api", None)
    print(host, api)
    if host is None or api is None:
        logger.warning(
            "[ RADARR ]",
            "Warning: {Warning}",
            Warning=" the radarr application is not configured in the yaml file ",
        )
        return

    try:
        # Initialize Radarr API
        radarr_api = RadarrAPI(host, api)

        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
        logger.info("[ RADARR ]", "Movie trailer finder started.")

        # Iterate through all movies in Radarr
        for movie in radarr_api.get_movie():
            print(movie)
            assert isinstance(movie, dict)

            path = movie.get("path", None)
            title = movie.get("title", None)
            year = movie.get("year", None)

            if path is None or title is None:
                # radarr item dont have path or title
                continue

            movie["outputs_folder"] = os.path.join(
                movie["path"], config["dir_backdrops"]
            )

            custom_path = config.get("custom_path", None)
            custom_name_movie = config.get("custom_name_movie", None)

            if custom_path and custom_name_movie:
                movie["outputs_folder"] = os.path.join(
                    custom_path, custom_name_movie, title
                )

            outputs_folder = movie["outputs_folder"]
            # create ooutputs folder if not exist
            os.makedirs(outputs_folder, exist_ok=True)

            # Skip if not enough space
            if not utils.check_space(outputs_folder):
                continue

            logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
            
            # outputs list dir 
            listdir = os.listdir(outputs_folder)
            
            # count trailers in ouputs
            count = len(listdir)
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

            # Fetch trailers using TMDB ID
            trailers = utils.trailer_pull(movie["tmdbId"], "movie")
            # No trailers found
            # fix :add here youtube search keyword
            if len(trailers) == 0:
                logger.warning(
                    "\t ->",
                    "No trailer is available for {title} ({year})",
                    title=title,
                    year=year,
                )
                continue
            else:
                list_of_trailers = utils.check_existing_trailer(trailers, listdir)
                utils.trailer_download(list_of_trailers, movie)

        logger.info("[ RADARR ]", "Movie trailer finder ended.")
        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
    except Exception as err:
        logger.error("[ RADARR ]", "An error occurred: {error}", error=err)
