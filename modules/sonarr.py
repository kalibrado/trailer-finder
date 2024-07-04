"""
modules/sonarr.py

This module interacts with Sonarr API to find and download trailers for TV series.
"""

import os
from pyarr import SonarrAPI
import modules.utils as ut


def sonarr():
    """
    Main function to find and download trailers for TV series using Sonarr API.
    """
    sonarr_api = SonarrAPI(ut.config["sonarr_host"], ut.config["sonarr_api"])
    ut.log(ut.WHITE, "[ SONARR ]", "Show trailer finder started.")

    for show in sonarr_api.get_series():
        if not os.path.exists(show["path"]):
            ut.log(
                ut.RED,
                "\t -> SCAN",
                "{title} ({year}) has no folder.",
                title=show["title"],
                year=show["year"],
            )
            continue

        if not ut.check_space(show["path"]):
            continue  # Move to the next series if space is insufficient

        ut.log(
            ut.WHITE,
            "\t -> SCAN",
            "Looking for {title} ({year}) trailers",
            title=show["title"],
            year=show["year"],
        )
        trailer_dir = os.path.join(show["path"], ut.config["output_dirs"])

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
                if trailer_count > 0:
                    ut.log(
                        ut.GREEN,
                        "\t -> SCAN",
                        "{title} ({year}) already has trailers.",
                        title=show["title"],
                        year=show["year"],
                    )
                    continue  # Move to the next series

            else:
                # If trailer_dir doesn't exist, move to the next series
                ut.log(
                    ut.RED,
                    "\t -> SCAN",
                    "{title} ({year}) has no trailer folder.",
                    title=show["title"],
                    year=show["year"],
                )
                continue

        # If only_one_trailer is False or no trailers found in trailer_dir
        episodes = ut.trailer_pull(show["imdbId"], "tv", parent_mode=True)
        for episode in episodes:
            episode_trailers = ut.trailer_pull(episode["id"], "tv")
            if episode_trailers:
                ut.trailer_download(episode_trailers, show)

    ut.log(ut.WHITE, "[ SONARR ]", "Show trailer finder ended.")
