"""
Module for logging messages with different severity levels and language localization.

This module defines a `Logger` class that extends the `Translator` class to log messages
with colors representing different severity levels (info, success, warning, error, debug).

Attributes:
    RESET (str): ANSI escape code to reset text color to default.
    RED (str): ANSI escape code for red text (error messages).
    GREEN (str): ANSI escape code for green text (success messages).
    WARN (str): ANSI escape code for yellow text (warning messages).
    WHITE (str): ANSI escape code for white text (info messages).

Classes:
    Logger: Extends the Translator class to log messages with different severity levels.

Usage example:

    # Importing the Logger class
    from modules.logger import Logger

    # Initializing the logger
    logger = Logger()

    # Logging an informational message
    logger.info("Downloading", "Started downloading movie trailers.")

    # Logging a success message
    logger.success("Downloaded", "Successfully downloaded trailer {trailer_name}.", trailer_name="Movie Trailer")

    # Logging a warning message
    logger.warning("File not found", "The file {file_path} does not exist.", file_path="/path/to/file.txt")

    # Logging an error message
    logger.error("File read error", "Failed to read file {file_name}.", file_name="example.txt")

"""

from time import sleep
import sys
from datetime import datetime
from modules.translator import Translator

# Console colors for log messages
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
WARN = "\033[0;33m"
WHITE = "\033[37m"


class Logger(Translator):
    """
    Logger class that extends the Translator class to log messages with different severity levels.

    Attributes:
        APP_TRANSLATE (str): The default language locale for translations.
    """

    def __init__(self, local="en", date_format="%Y-%m-%d %H:%M:%S"):
        """
        Initializes the Logger with a default locale.

        Args:
            local (str): The default language locale for translations. Default is 'en'.
        """
        super().__init__(local)
        self.date_format = date_format

    def _log(self, color: str, msg: str):
        """
        Logs a message to the console with the specified color.

        Args:
            color (str): The color code for the message.
            msg (str): The message to log.
        """
        current_time = datetime.now().strftime(self.date_format)
        sys.stdout.write(f"[ {current_time} ] -> {color} {msg} {RESET} \n")
        sys.stdout.flush()
        sleep(0.5)  # Wait 0.5s to avoid excessive CPU load

    def info(self, msg_key="", **kwargs):
        """
        Logs an informational message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional arguments for the translation.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(WHITE, msg)

    def success(self, msg_key="", **kwargs):
        """
        Logs a success message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional arguments for the translation.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(GREEN, msg)

    def warning(self, msg_key="", **kwargs):
        """
        Logs a warning message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional arguments for the translation.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(WARN, msg)

    def error(self, msg_key="", **kwargs):
        """
        Logs an error message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional arguments for the translation.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(RED, msg)
