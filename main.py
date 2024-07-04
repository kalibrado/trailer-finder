""" main.py """

from time import sleep
from modules.sonarr import sonarr
from modules.radarr import radarr
from modules.utils import log, WHITE, RED, config


def main():
    """
    Main function to run Sonarr and Radarr processes.

    This function runs a loop that executes Radarr and Sonarr processes
    to find and download trailers for movies and TV shows.
    It logs the start and end of the process and sleeps for a specified
    duration between each run.
    """
    while True:
        log(WHITE, "[ MAIN ]", "Starting trailer finder.")

        try:
            radarr()
        except Exception as e:
            log(RED, "[ MAIN ]", "An error occurred: {error}", error=f"Radarr {e}")

        try:
            sonarr()
        except Exception as e:
            log(RED, "[ MAIN ]", "An error occurred: {error}", error=f"Sonarr {e}")

        log(
            WHITE, "[ MAIN ]", "Sleeping for {hours} hours.", hours=config["sleep_time"]
        )
        sleep(config["sleep_time"] * 3600)


if __name__ == "__main__":
    main()
