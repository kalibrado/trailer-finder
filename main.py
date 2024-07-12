""" main.py """

import os
import sys
from time import sleep
import yaml
from modules.sonarr import sonarr
from modules.radarr import radarr
from modules.logger import Logger
from modules.utils import Utils


def main():
    """
    Main function to run Sonarr and Radarr processes.

    This function runs a loop that executes Radarr and Sonarr processes
    to find and download trailers for movies and TV shows.
    It logs the start and end of the process and sleeps for a specified
    duration between each run.
    """
    # Initialize Logger with configuration parameters
    logger = Logger()
    if not os.path.exists("config/config.yaml"):
        # Log an error if the configuration file does not exist
        logger.error(
            "[ MAIN ]",
            "File {name} is not exist in {path}",
            name="config.yaml",
            path="config/",
        )
        return

    # Load configuration from the YAML file
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        logger = Logger(default_locale=config["default_locale"])
        utils = Utils(logger, config)
        module_err = {"sonarr": None, "radarr": None}
        while True:
            # Log the start of the trailer finding process
            logger.info("[ MAIN ]", "Starting trailer finder.")

            try:
                # Run the Radarr process
                radarr(logger, config, utils)
            except Exception as e:
                # Catch and log any exceptions that occur in the Radarr process
                module_err["radarr"] = f"Radarr: {e}"

            try:
                # Run the Sonarr process
                sonarr(logger, config, utils)
            except Exception as e:
                # Catch and log any exceptions that occur in the Sonarr process
                module_err["sonarr"] = f"Sonarr: {e}"

            # Log errors if both Radarr and Sonarr fail, then exit the script
            if module_err["radarr"] and module_err["sonarr"]:
                logger.error(
                    "[ MAIN ]",
                    "An error occurred: {error}",
                    error=f"\n{module_err['radarr']} \n{module_err['sonarr']} ",
                )
                sys.exit()

            # Log warnings if either Radarr or Sonarr fails
            if module_err["radarr"] or module_err["sonarr"]:
                logger.warning(
                    "[ MAIN ]",
                    "Warning: {Warning}",
                    Warning=f" {module_err['radarr']} {module_err['sonarr']} ",
                )

            logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
            # Sleep for the specified duration before the next run
            time = config["sleep_time"]
            logger.info("[ MAIN ]", "Waiting for {hours} hours.", hours=time)
            sleep(time * 3600)
            os.system("clear")


if __name__ == "__main__":
    os.system("clear")
    # Print a welcome ASCII art
    print(
        r"""
████████╗██████╗  █████╗ ██╗██╗     ███████╗██████╗       ███████╗██╗███╗   ██╗██████╗ ███████╗██████╗                                   
╚══██╔══╝██╔══██╗██╔══██╗██║██║     ██╔════╝██╔══██╗      ██╔════╝██║████╗  ██║██╔══██╗██╔════╝██╔══██╗                                  
   ██║   ██████╔╝███████║██║██║     █████╗  ██████╔╝█████╗█████╗  ██║██╔██╗ ██║██║  ██║█████╗  ██████╔╝                                  
   ██║   ██╔══██╗██╔══██║██║██║     ██╔══╝  ██╔══██╗╚════╝██╔══╝  ██║██║╚██╗██║██║  ██║██╔══╝  ██╔══██╗                                  
   ██║   ██║  ██║██║  ██║██║███████╗███████╗██║  ██║      ██║     ██║██║ ╚████║██████╔╝███████╗██║  ██║                                  
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚═╝  ╚═╝      ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ ╚══════╝╚═╝  ╚═╝                                  
                                                ██████╗ ██╗   ██╗    ██╗  ██╗ █████╗ ██╗     ██╗██████╗ ██████╗  █████╗ ██████╗  ██████╗ 
                                                ██╔══██╗╚██╗ ██╔╝    ██║ ██╔╝██╔══██╗██║     ██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██╔═══██╗
                                                ██████╔╝ ╚████╔╝     █████╔╝ ███████║██║     ██║██████╔╝██████╔╝███████║██║  ██║██║   ██║
                                                ██╔══██╗  ╚██╔╝      ██╔═██╗ ██╔══██║██║     ██║██╔══██╗██╔══██╗██╔══██║██║  ██║██║   ██║
                                                ██████╔╝   ██║       ██║  ██╗██║  ██║███████╗██║██████╔╝██║  ██║██║  ██║██████╔╝╚██████╔╝
                                                ╚═════╝    ╚═╝       ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ 
                                                                                                                                         
"""
    )
    main()
