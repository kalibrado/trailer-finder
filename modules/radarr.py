"""
modules/radarr.py

This module interacts with the Radarr API to find and download trailers for movies.

Classes:
    None

Functions:
    radarr(logger: Logger, config: dict, utils: Utils) -> None:
        Main function to find and download trailers for movies using the Radarr API.

Usage Example:

    # Importing the radarr function
    from modules.radarr import radarr

    # Initialize a logger instance (assuming 'logger' is already initialized)
    logger = Logger()

    # Example configuration dictionary
    config = {
        "RADARR_HOST": "http://localhost:7878",  # Radarr host URL
        "RADARR_API": "your_api_key_here",  # Radarr API key
        "APP_DEFAULT_DIR": "trailers",  # Default directory for saving trailers
        "APP_CUSTOM_PATH": "/custom/path",  # Custom path for saving trailers (optional)
        "APP_CUSTOM_NAME_MOVIE": "movie_trailers",  # Custom directory name for trailers (optional)
        "APP_ONLY_ONE_TRAILER": True,  # Download only one trailer per movie (optional)
    }

    # Initialize an instance of your Utils class (assuming 'utils' is already initialized)
    utils = Utils()

    # Call the radarr function to find and download trailers
    radarr(logger, config, utils)

    # Example output folder structure:
    # Assuming the output folder structure is based on the movie title and year

"""

import os
from pyarr import RadarrAPI
from modules.logger import Logger
from modules.utils import Utils


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
        logger.warning("[ RADARR ]", "Warning: {warning}", Warning=" the radarr application is not configured in the yaml file ")
        return

    try:
        # Initialize Radarr API
        radarr_api = RadarrAPI(host, api)

        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
        logger.info("[ RADARR ]", "Movie trailer finder started.")

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
                logger.error("[ RADARR ]", "Warning: {warning}", warning=f"Path or Title not exist in: {movie}")
                continue

            movie["outputs_folder"] = os.path.join(movie["path"], config["APP_DEFAULT_DIR"])

            custom_path = config.get("APP_CUSTOM_PATH", None)
            custom_name = config.get("APP_CUSTOM_NAME_MOVIE", None)

            if custom_path and custom_name:
                movie["outputs_folder"] = os.path.join(custom_path, custom_name, title)

            outputs_folder = movie["outputs_folder"]
            # create ooutputs folder if not exist
            os.makedirs(outputs_folder, exist_ok=True)

            # Skip if not enough space
            if not utils.check_space(outputs_folder):
                continue

            logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")

            # outputs list dir
            trailers_in_outputs_folder = os.listdir(outputs_folder)

            # count trailers in ouputs
            count = len(trailers_in_outputs_folder)

            # Skip if trailer already exists
            if config["APP_ONLY_ONE_TRAILER"] and count >= 1:
                logger.success("\t ->", "{title} ({year}) already has {count} trailers.", title=title, year=year, count=count)
                continue

            logger.info("\t ->", "Looking for {title} ({year}) trailers", title=title, year=year)
            # Fetch trailers using TMDB ID
            movie["query_type"] = "TMDB API"
            trailers = utils.trailer_pull(movie["tmdbId"], "movie")
            list_of_trailers = utils.get_new_trailers(trailers, trailers_in_outputs_folder)
            # No trailers found
            if len(list_of_trailers) == 0:
                logger.warning("\t\t ->", "No trailers available on {query}", query=movie["query_type"])
                link = {
                    "name": movie["use_title"],
                    "yt_link": f"gvsearch5:{movie['use_title']} {config.get('YT_DLP_SEARCH_KEYWORD')}",
                }
                list_of_trailers = [link]
                logger.info("\t\t ->", "Search trailer with {query}", query=link["yt_link"])
                movie["query_type"] = link["yt_link"]
            utils.download_trailers(list_of_trailers, movie)

        logger.info("[ RADARR ]", "Movie trailer finder ended.")
        logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
    except Exception as err:
        logger.error("[ RADARR ]", "An error occurred: {error}", error=err)
