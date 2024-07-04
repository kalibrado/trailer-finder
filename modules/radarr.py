"""
modules/radarr.py

This module interacts with the Radarr API to find and download trailers for movies.
"""

import os
from pyarr import RadarrAPI
import modules.utils as ut


def radarr():
    """
    Main function to find and download trailers for movies using the Radarr API.
    """
    radarr_api = RadarrAPI(ut.config["radarr_host"], ut.config["radarr_api"])
    ut.log(ut.WHITE, "[ RADARR ]", "Movie trailer finder started.")

    for movie in radarr_api.get_movie():
        if not os.path.exists(movie["path"]) or not ut.check_space(movie["path"]):
            continue

        ut.log(
            ut.WHITE,
            "\t -> SCAN",
            "Looking for {title} ({year}) trailers",
            title=movie["title"],
            year=movie["year"],
        )
        trailer_dir = os.path.join(movie["path"], ut.config["output_dirs"])

        if ut.config["only_one_trailer"]:
            if os.path.exists(trailer_dir):
                # Check the number of existing trailer files in trailer_dir
                trailer_count = len(
                    [
                        file
                        for file in os.listdir(trailer_dir)
                        if file.endswith("." + ut.config["filetype"])
                    ]
                )

                if trailer_count > 1:
                    ut.log(
                        ut.GREEN,
                        "\t -> SCAN",
                        "{title} ({year}) already has a trailer.",
                        title=movie["title"],
                        year=movie["year"],
                    )
                    continue  # Move to the next movie

                trailers = ut.trailer_pull(movie["tmdbId"], "movie")
                if len(trailers) == 0:
                    continue
                ut.trailer_download(
                    ut.check_existing_trailer(trailers, os.listdir(trailer_dir)), movie
                )

            else:
                # If trailer_dir doesn't exist, move to the next movie
                ut.log(
                    ut.RED,
                    "\t -> SCAN",
                    "{title} ({year}) has no trailer folder.",
                    title=movie["title"],
                    year=movie["year"],
                )
                continue

        else:  # If only_one_trailer is False
            if os.path.exists(trailer_dir) and os.listdir(trailer_dir):
                trailers = ut.trailer_pull(movie["tmdbId"], "movie")
                if len(trailers) == 0:
                    continue
                ut.trailer_download(
                    ut.check_existing_trailer(trailers, os.listdir(trailer_dir)), movie
                )
            else:
                # If trailer_dir doesn't exist or is empty, move to the next movie
                ut.log(
                    ut.RED,
                    "\t -> SCAN",
                    "{title} ({year}) has no trailer folder or trailers.",
                    title=movie["title"],
                    year=movie["year"],
                )
                continue
        ut.log(ut.BLUE, "\t", "{cmd}", cmd="--------------------------------")

    ut.log(ut.WHITE, "[ RADARR ]", "Movie trailer finder ended.")
