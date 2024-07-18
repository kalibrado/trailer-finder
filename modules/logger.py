"""
Module providing logging functionality for capturing messages during script execution.

This module defines the Logger class to handle logging messages with different levels of severity.
It supports writing logs to console and file based on configurations from `config.yaml`.

Dependencies:
    - logging: Standard Python logging module for logging messages.
    - datetime: Date and time handling.

Classes:
    - Logger:
        Class providing logging functionalities for capturing and formatting messages.

Attributes:
    log_path (str): Path to the log file where logs will be written.
    log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) based on configurations.

Usage:
    This module provides essential logging capabilities for capturing messages during script execution.
    It initializes the Logger class with configurations from `config.yaml` to define log file path and
    logging level. Ensure `config.yaml` is correctly configured with logging settings before running scripts.
"""

from time import sleep
import sys
from datetime import datetime
from modules.translator import Translator


class Logger(Translator):
    """
    Logger class that extends the Translator class to log messages with different severity levels.

    Attributes:
        APP_TRANSLATE (str): The default language locale for translations.
    """

    # Console colors for log messages
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    WARN = "\033[0;33m"
    WHITE = "\033[37m"

    def __init__(self, local="en", date_format="%Y-%m-%d %H:%M:%S"):
        """
        Initializes the Logger with a default locale and date format.

        Args:
            local (str, optional): The default language locale for translations. Defaults to 'en'.
            date_format (str, optional): The format for date and time in log messages. Defaults to "%Y-%m-%d %H:%M:%S".
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
        sys.stdout.write(f"[ {current_time} ] -> {color} {msg} {self.RESET} \n")
        sys.stdout.flush()
        sleep(0.5)  # Wait 0.5s to avoid excessive CPU load

    def info(self, msg_key="", **kwargs):
        """
        Logs an informational message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(self.WHITE, msg)

    def success(self, msg_key="", **kwargs):
        """
        Logs a success message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(self.GREEN, msg)

    def warning(self, msg_key="", **kwargs):
        """
        Logs a warning message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(self.WARN, msg)

    def error(self, msg_key="", **kwargs):
        """
        Logs an error message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(self.RED, msg)
