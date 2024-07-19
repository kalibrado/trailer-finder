"""
Main script to run Sonarr and Radarr processes for finding and downloading trailers.

This script executes Sonarr and Radarr processes in a loop to find and download trailers
for both TV shows and movies. It utilizes configurations from 'config/config.yaml' for
customizing settings such as API keys, file paths, and sleep duration between runs.
Events and errors are logged using a Logger instance configured with localization and
date formatting settings from the configuration file.

Dependencies:
    - os: Operating system interface for file operations and clearing console screen.
    - sys: System-specific parameters and functions.
    - time.sleep: Function to pause execution for a specified amount of time.
    - yaml: Library for reading YAML configuration files.
    - modules.sonarr.sonarr: Module for interacting with Sonarr API to find and download TV show trailers.
    - modules.radarr.radarr: Module for interacting with Radarr API to find and download movie trailers.
    - modules.logger.Logger: Logger instance for logging messages with custom formatting and color output.
    - modules.utils.Utils: Utility functions instance for handling trailer downloads and processing.
    - modules.exceptions.FfmpegError: Exception raised for errors related to FFMPEG processing.
    - modules.exceptions.FfmpegCommandMissing: Exception raised when FFMPEG command is missing in configuration.
    - modules.exceptions.InvalidLogLevelError: Exception raised for invalid logging levels.
    - modules.exceptions.InvalidLogCountError: Exception raised for invalid log backup count.
    - modules.exceptions.InvalidLogSizeError: Exception raised for invalid log file size.

Functions:
    - main():
        Main function to run Sonarr and Radarr processes for finding and downloading trailers.

Usage:
    This script is intended to be executed directly to continuously run processes that find and
    download trailers for movies and TV shows managed by Radarr and Sonarr respectively. It uses
    configurations from 'config/config.yaml' to customize behavior such as file paths, API keys,
    and sleep duration between runs. Ensure 'config/config.yaml' is correctly configured before
    running the script.

Example:
    To run this script:
    ```bash
    python main.py
    ```
    Ensure 'config/config.yaml' is present and correctly configured to avoid errors during execution.

Error Handling:
    - If the configuration file 'config/config.yaml' is missing or incorrectly defined, the script will exit with an error message.
    - The script raises specific exceptions with translated messages if there are issues with logging configuration:
        - `InvalidLogLevelError`: Raised for invalid logging levels in the configuration.
        - `InvalidLogCountError`: Raised for invalid log backup count in the configuration.
        - `InvalidLogSizeError`: Raised for invalid log file size in the configuration.
    - The script also handles exceptions related to FFMPEG processing and general program interruptions.
"""

import os
import sys
from time import sleep
import yaml
from modules.sonarr import sonarr
from modules.radarr import radarr
from modules.logger import Logger
from modules.utils import Utils
from modules.exceptions import FfmpegError, FfmpegCommandMissing, InvalidLogLevelError, InvalidLogCountError, InvalidLogSizeError


def main():
    """
    Main function to run Sonarr and Radarr processes.

    This function runs a loop that executes Radarr and Sonarr processes
    to find and download trailers for movies and TV shows.
    It logs the start and end of the process and sleeps for a specified
    duration between each run.
    """

    # Check if the configuration file exists
    if not os.path.exists("config/config.yaml"):
        # Log an error if the configuration file does not exist and terminate the script
        print("The configuration file is not found or is poorly defined in config/config.yml")
        print("For information on using this script, please refer to the documentation. => https://kalibrado.github.io/trailer-finder/ ")
        sys.exit(1)

    # Load configuration from the YAML file
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

        try:
            # Initialize Logger with a specific localization setting from config.yaml
            logger = Logger(
                local=config.get("APP_TRANSLATE"),
                date_format=config.get("APP_LOG_DATE_FORMAT"),
                log_path=config.get("APP_LOG_PATH"),
                log_level=config.get("APP_LOG_LEVEL"),
                log_backup_count=config.get("APP_LOG_BACKUP_COUNT"),
                log_max_size=config.get("APP_LOG_MAX_SIZE"),
            )
        except (InvalidLogLevelError, InvalidLogCountError, InvalidLogSizeError) as err:
            print(err)
            sys.exit(1)

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
                logger.info("Please wait for {hours} hours.", hours=time)
                sleep(time * 3600)  # Convert hours to seconds for sleep function

                # Clear the console screen for better readability
                os.system("clear")

        except (
            FfmpegError,
            FfmpegCommandMissing,
            InvalidLogLevelError,
            InvalidLogCountError,
            InvalidLogSizeError,
        ) as err:
            logger.error("An error has occurred: {error}.", error=err)

        except KeyboardInterrupt:
            logger.error("Program interruption detected. Shutdown in progress...")

        finally:
            sys.exit(0)


if __name__ == "__main__":
    # Start the main function
    main()
