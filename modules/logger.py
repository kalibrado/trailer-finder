"""
Module providing enhanced logging functionality with support for custom date formats and color-coded console output.

This module defines the `Logger` class, which extends the `Translator` class to provide logging capabilities with
customizable date formats and color-coded console messages. The `Logger` class supports logging messages with
different levels of severity and can write logs to both the console and a file. It also includes support for log
rotation based on file size and backup count.

Dependencies:
    - `logging`: Standard Python logging module for logging messages.
    - `logging.handlers`: Provides handlers for logging, including rotating file handlers.
    - `sys`: Provides access to system-specific parameters and functions.
    - `os`: Provides a portable way of using operating system-dependent functionality.
    - `time`: Provides time-related functions.
    - `modules.translator`: Custom module for handling message translations.
    - `modules.colored_formatter`: Custom module defining the `ColoredFormatter` class for color-coded logging.

Classes:
    - `Logger`:
        A logging class that extends the `Translator` class to handle logging messages with custom formatting and color output.

Attributes:
    - `local` (str): The default language locale for translations.
    - `date_format` (str): Format for date and time in log messages.
    - `log_path` (str): Path to the log file where logs will be written. If not specified, logs are only output to the console.
    - `log_level` (str): Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`) to control which messages are logged.
    - `log_max_size` (int): Maximum size of the log file before rotation occurs, specified in megabytes.
    - `log_backup_count` (int): Number of backup files to keep when rotating logs.

Usage:
    Initialize the `Logger` class with parameters to set up logging configurations such as file path, log level,
    date format, maximum file size, and backup count. Logs can be written to the console and/or a file, and messages
    will be color-coded based on their severity level in the console.

    Example configuration:

    .. code-block:: python

        logger = Logger(
            local="en",
            date_format="%Y-%m-%d %H:%M:%S",
            log_path="path/to/logfile.log",
            log_level="INFO",
            log_max_size=10,  # in megabytes
            log_backup_count=5
        )

    Log methods:
        - `info(msg_key="", **kwargs)`: Logs an informational message.
        - `success(msg_key="", **kwargs)`: Logs a success message.
        - `warning(msg_key="", **kwargs)`: Logs a warning message.
        - `error(msg_key="", **kwargs)`: Logs an error message.
        - `debug(msg_key="", **kwargs)`: Logs a debug message.
        - `critical(msg_key="", **kwargs)`: Logs a critical message.

    Error Handling:
        The `Logger` class raises specific exceptions with translated messages when invalid parameters are provided:
        - `InvalidLogSizeError`: Raised if `log_max_size` is not a positive integer.
        - `InvalidLogCountError`: Raised if `log_backup_count` is not a non-negative integer.
        - `InvalidLogLevelError`: Raised if `log_level` is not one of the valid logging levels (`DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`).
"""

import sys
import os
import logging
import logging.handlers
from time import sleep
from modules.translator import Translator
from modules.colored_formatter import ColoredFormatter
from modules.exceptions import InvalidLogLevelError, InvalidLogCountError, InvalidLogSizeError


class Logger(Translator):
    """
    Logger class that extends the Translator class to handle logging messages with custom formatting and color output.

    Attributes:
        local (str): The default language locale for translations.
        date_format (str): Format for date and time in log messages.
        log_path (str): Path to the log file where logs will be written. If not specified, logs are only output to the console.
        log_level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) to control which messages are logged.
        log_max_size (int): Maximum size of the log file before rotation occurs, specified in bytes.
        log_backup_count (int): Number of backup files to keep when rotating logs.
    """

    def __init__(self, local="en", date_format="%Y-%m-%d %H:%M:%S", log_path=None, log_level="INFO", log_max_size=10, log_backup_count=5):
        """
        Initializes the Logger with a default locale, date format, and logging configuration.

        Args:
            local (str, optional): The default language locale for translations. Defaults to 'en'.
            date_format (str, optional): The format for date and time in log messages. Defaults to "%Y-%m-%d %H:%M:%S".
            log_path (str, optional): Path to the log file. If None, logs are not written to a file. Defaults to None.
            log_level (str, optional): The logging level. Defaults to "INFO". Valid values are DEBUG, INFO, WARNING, ERROR, CRITICAL.
            log_max_size (int, optional): Maximum log file size before rotation in megabytes. Defaults to 10.
            log_backup_count (int, optional): Number of backup files to keep. Defaults to 5.
        """
        super().__init__(local)

        if not isinstance(log_max_size, int) or log_max_size <= 0:
            raise InvalidLogSizeError(
                self.translate(
                    "The size of the defined logs in the config file is not valid « {size} ».",
                    size=log_max_size,
                )
            )
        if not isinstance(log_backup_count, int):
            raise InvalidLogCountError(
                self.translate(
                    "The number of logs saved in the configuration file is not a valid format « {count} ».",
                    count=log_backup_count,
                )
            )

        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if log_level.upper() not in valid_levels:
            raise InvalidLogLevelError(
                self.translate(
                    "The defined log level « {log} » is not valid. The valid log type is « {levels} ».",
                    log=log_level,
                    levels=", ".join(valid_levels),
                )
            )

        self.date_format = date_format
        self.log_path = log_path
        self.log_level = log_level.upper()
        self.log_max_size = log_max_size * 1024 * 1024  # Convert MB to bytes
        self.log_backup_count = log_backup_count
        self._setup_logging()

    def _setup_logging(self) -> None:
        """
        Sets up logging configuration based on provided log_path, log_level, log_max_size, and log_backup_count.
        """
        log_level = getattr(logging, self.log_level, logging.INFO)
        formatter = ColoredFormatter("%(asctime)s - %(levelname)s - %(message)s", datefmt=self.date_format)

        logger = logging.getLogger()
        logger.setLevel(log_level)

        # Remove all existing handlers
        if logger.hasHandlers():
            logger.handlers.clear()

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        logger.addHandler(console_handler)

        # File handler
        if self.log_path:
            try:
                os.makedirs(os.path.dirname(self.log_path), exist_ok=True)
                file_handler = logging.handlers.RotatingFileHandler(self.log_path, maxBytes=self.log_max_size, backupCount=self.log_backup_count)
                file_handler.setFormatter(formatter)
                file_handler.setLevel(log_level)
                logger.addHandler(file_handler)
            except Exception as e:
                print(f"Failed to set up file logging: {e}", file=sys.stderr)

    def _log(self, level: str, msg: str) -> None:
        """
        Logs a message to the console and/or file with the specified level and color.

        Args:
            level (str): The logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
            msg (str): The message to log.
        """
        log_func = getattr(logging, level.lower())
        log_func(msg)
        sleep(1)  # Wait 1s to avoid excessive CPU load

    def info(self, msg_key: str = "", **kwargs) -> None:
        """
        Logs an informational message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("INFO", msg)

    def success(self, msg_key: str = "", **kwargs) -> None:
        """
        Logs a success message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("INFO", msg)

    def warning(self, msg_key: str = "", **kwargs) -> None:
        """
        Logs a warning message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("WARNING", msg)

    def error(self, msg_key: str = "", **kwargs) -> None:
        """
        Logs an error message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("ERROR", msg)

    def debug(self, msg_key: str = "", **kwargs) -> None:
        """
        Logs a debug message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("DEBUG", msg)

    def critical(self, msg_key: str = "", **kwargs) -> None:
        """
        Logs a critical message.

        Args:
            msg_key (str): The key for the message to translate.
            **kwargs: Additional keyword arguments to format the translated message.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log("CRITICAL", msg)
