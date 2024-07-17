"""
main.py

This script runs Sonarr and Radarr processes to find and download trailers for movies and TV shows.
It utilizes configuration from 'config/config.yaml' and logs events using a Logger instance.
"""

import os
import sys
from time import sleep
import yaml
from modules.sonarr import sonarr
from modules.radarr import radarr
from modules.logger import Logger
from modules.utils import Utils
from modules.exceptions import FfmpegError, FfmpegCommandMissing


def main():
    """
    Main function to run Sonarr and Radarr processes.

    This function runs a loop that executes Radarr and Sonarr processes
    to find and download trailers for movies and TV shows.
    It logs the start and end of the process and sleeps for a specified
    duration between each run.
    """
    # Initialize Logger with default settings
    logger = Logger()

    # Check if the configuration file exists
    if not os.path.exists("config/config.yaml"):
        # Log an error if the configuration file does not exist and terminate the script
        logger.error("File {name} not exist in {path}", name="config.yaml", path="config/")
        return

    # Load configuration from the YAML file
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

        # Initialize Logger with a specific localization setting from config.yaml
        logger = Logger(local=config.get("APP_TRANSLATE"), date_format=config.get("APP_LOG_DATE_FORMAT"))

        # Initialize Utils object to provide utility methods for operations
        utils = Utils(logger, config)
        try:
            # Infinite loop to continuously run the processes
            while True:
                # Log the start of the trailer finding process
                logger.info("Starting trailers finder.")

                # Run the Radarr process to find and download movie trailers
                radarr(logger, config, utils)

                # Run the Sonarr process to find and download TV show trailers
                sonarr(logger, config, utils)

                # Log a separator line between runs
                print("--------------------------------")

                # Sleep for the specified duration before the next run
                time = config["APP_SLEEP_TIME"]
                logger.info("Please wait for « {hours} » hours.", hours=time)
                sleep(time * 3600)  # Convert hours to seconds for sleep function
                # Clear the console screen for better readability
                os.system("clear")
        except (FfmpegError, FfmpegCommandMissing) as err:
            logger.error("An error has occurred: {error}.", error=err)
        except KeyboardInterrupt:
            logger.error("Program interruption detected. Shutdown in progress...")
        finally:
            sys.exit(0)


if __name__ == "__main__":
    # Start the main function
    main()
