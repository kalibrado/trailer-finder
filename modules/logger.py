"""
Module providing logging functionality for capturing messages during script execution.

This module defines the Logger class to handle logging messages with different levels of severity.
It supports writing logs to both the console and a file based on configurations provided during initialization.

Dependencies:
    - logging: Standard Python logging module for logging messages.
    - datetime: Date and time handling.

Classes:
    - Logger:
        Class providing logging functionalities for capturing and formatting messages.

Attributes:
    log_path (str): Path to the log file where logs will be written. If not specified, logs are not written to a file.
    log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) based on configurations.

Methods:
    - __init__(self, local="en", date_format="%Y-%m-%d %H:%M:%S", log_path=None, log_level="INFO"):
        Initializes the Logger with default settings or provided configuration.

    - _setup_logging(self):
        Configures the logging handlers based on provided log_path and log_level.

    - _log(self, level: str, color: str, msg: str):
        Logs a message to the console and/or file with the specified level and color.

    - debug(self, msg_key="", **kwargs):
        Logs a debug message with blue color to the console and file if configured.

    - info(self, msg_key="", **kwargs):
        Logs an informational message with white color to the console and file if configured.

    - success(self, msg_key="", **kwargs):
        Logs a success message with green color to the console and file if configured.

    - warning(self, msg_key="", **kwargs):
        Logs a warning message with yellow color to the console and file if configured.

    - error(self, msg_key="", **kwargs):
        Logs an error message with red color to the console and file if configured.

    - critical(self, msg_key="", **kwargs):
        Logs a critical message with magenta color to the console and file if configured.

Usage:
    This module provides essential logging capabilities for capturing messages during script execution.
    It initializes the Logger class with parameters to define log file path and logging level.
    Ensure to configure the logger correctly to capture and format log messages as needed.

Example:
    To use this module, create an instance of the Logger class with desired configurations:

    ```python
    logger = Logger(
        local="en",
        date_format="%Y-%m-%d %H:%M:%S",
        log_path="path/to/logfile.log",
        log_level="DEBUG"
    )
    ```

    You can then use the logger instance to log messages at various levels:

    ```python
    logger.info("This is an info message.")
    logger.error("This is an error message.")
    logger.debug("This is a debug message.")
    logger.critical("This is a critical message.")
    ```

    The messages will be logged to both the console and the specified log file, with color coding for console output based on the severity level.
"""

import sys
import os
import logging
from datetime import datetime
from modules.translator import Translator
from time import sleep


class Logger(Translator):
    """
    Logger class that extends the Translator class to log messages with different severity levels.

    Attributes:
        APP_TRANSLATE (str): The default language locale for translations.
        log_path (str): Path to the log file where logs will be written.
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
    """

    # Console colors for log messages
    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    WARN = "\033[0;33m"
    WHITE = "\033[37m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"

    def __init__(self, local="en", date_format="%Y-%m-%d %H:%M:%S", log_path=None, log_level="INFO"):
        """
        Initializes the Logger with a default locale, date format, and logging configuration.

        Args:
            local (str, optional): The default language locale for translations. Defaults to 'en'.
            date_format (str, optional): The format for date and time in log messages. Defaults to "%Y-%m-%d %H:%M:%S".
            log_path (str, optional): Path to the log file. If None, logs are not written to a file. Defaults to None.
            log_level (str, optional): The logging level. Defaults to "INFO". Valid values are DEBUG, INFO, WARNING, ERROR, CRITICAL.
        """
        super().__init__(local)
        self.date_format = date_format
        self.log_path = log_path
        self.log_level = log_level.upper()
        self._setup_logging()

    def _setup_logging(self):
        """
        Sets up logging configuration based on provided log_path and log_level.
        """
        log_level = getattr(logging, self.log_level, logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)

        # File handler
        if self.log_path:
            os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
            file_handler = logging.FileHandler(self.log_path)
            file_handler.setFormatter(formatter)
            file_handler.setLevel(log_level)
            logging.getLogger().addHandler(file_handler)

        logging.getLogger().addHandler(console_handler)
        logging.getLogger().setLevel(log_level)

    def _log(self, level: str, color: str, msg: str):
        """
        Logs a message to the console and/or file with the specified level and color.

        Args:
            level (str): The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            color (str): The color code for the message.
            msg (str): The message to log.
        """
        log_func = getattr(logging, level.lower())
        log_func(msg)

        # Log to console with color
        current_time = datetime.now().strftime(self.date_format)
        sys.stdout.write(f"[ {current_time} ] -> {color} {msg} {self.RESET} \n")
        sys.stdout.flush()
        sleep(0.5)  # Wait 0.5s to avoid excessive CPU load

    def debug(self, msg_key="", **kwargs):
        """
        Logs a debug message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("DEBUG", self.BLUE, msg)

    def info(self, msg_key="", **kwargs):
        """
        Logs an informational message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("INFO", self.WHITE, msg)

    def success(self, msg_key="", **kwargs):
        """
        Logs a success message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("INFO", self.GREEN, msg)

    def warning(self, msg_key="", **kwargs):
        """
        Logs a warning message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("WARNING", self.WARN, msg)

    def error(self, msg_key="", **kwargs):
        """
        Logs an error message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("ERROR", self.RED, msg)

    def critical(self, msg_key="", **kwargs):
        """
        Logs a critical message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("CRITICAL", self.MAGENTA, msg)
