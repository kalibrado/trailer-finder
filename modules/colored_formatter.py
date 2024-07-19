"""
Custom formatter to add color to log messages based on their severity level.

This class extends `logging.Formatter` to provide colored output for log messages, allowing for visual differentiation
of log levels in the console.

Attributes:
    COLORS (dict): Dictionary mapping log levels to color codes.

Methods:
    format(record: logging.LogRecord) -> str:
        Format the log record with color based on its severity level.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with color.
"""


import logging


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter to add color to log messages based on their severity level.

    Attributes:
        COLORS (dict): Dictionary mapping log levels to color codes.
    """

    COLORS = {
        "DEBUG": "\033[34m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
        "RESET": "\033[0m",
    }

    def format(self, record):
        """
        Format the log record with color based on its severity level.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message with color.
        """
        color = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        reset = self.COLORS["RESET"]
        message = super().format(record)
        return f"{color}{message}{reset}"
