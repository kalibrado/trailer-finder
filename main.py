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
        logger.error(
            "[ MAIN ]",
            "File {name} is not exist in {path}",
            name="config.yaml",
            path="config/",
        )
        return

    # Load configuration
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)
        logger = Logger(default_locale=config["default_locale"])
        utils = Utils(logger, config)
        module_err = {"sonarr": None, "radarr": None}
        while True:
            logger.info("[ MAIN ]", "Starting trailer finder.")

            try:
                radarr(logger, config, utils)
            except Exception as e:
                module_err["radarr"] = f"Radarr: {e}"

            try:
                sonarr(logger, config, utils)
            except Exception as e:
                module_err["sonarr"] = f"Sonarr: {e}"

            if module_err["radarr"] and module_err["sonarr"]:
                logger.error(
                    "[ MAIN ]",
                    "An error occurred: {error}",
                    error=f"\n{module_err['radarr']} \n{module_err['sonarr']} ",
                )
                sys.exit()

            if module_err["radarr"] or module_err["sonarr"]:
                logger.warning(
                    "[ MAIN ]",
                    "Warning: {Warning}",
                    Warning=f" {module_err['radarr']} {module_err['sonarr']} ",
                )

            logger.info("\t", "{msg_gen}", msg_gen="--------------------------------")
            time = config["sleep_time"]
            logger.info("[ MAIN ]", "Waiting for {hours} hours.", hours=time)
            sleep(time * 3600)


if __name__ == "__main__":
    print(
        r"""\
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
                                                                                                                                         
""")
    main()
