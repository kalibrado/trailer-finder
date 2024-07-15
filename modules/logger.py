"""modules/logger.py"""

from time import sleep
import sys
from modules.translator import Translator

# Console colors for log messages
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
WARN = "\033[0;33m"
WHITE = "\033[37m"


class Logger(Translator):
    """
    Logger class that extends the Translator class to log messages with different severity levels.

    Attributes:
        default_locale (str): The default language locale for translations.
    """

    def __init__(self, default_locale="en"):
        """
        Initializes the Logger with a default locale.

        Args:
            default_locale (str): The default language locale for translations. Default is 'en'.
        """
        super().__init__(default_locale)

    def _log(self, color: str, msg: str):
        """
        Logs a message to the console with the specified color.

        Args:
            color (str): The color code for the message.
            msg (str): The message to log.
        """
        sys.stdout.write(f"{color} {msg} {RESET}")
        sys.stdout.write("\n")
        sys.stdout.flush()
        sleep(1)

    def info(self, prefix=" ", msg_key="", **kwargs):
        """
        Logs an informational message.

        Args:
            prefix (str): The prefix to add before the message. Default is a space.
            msg_key (str): The key for the message to translate.
            **kwargs: Additional arguments for the translation.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(WHITE, f"{prefix} {msg}")

    def success(self, prefix=" ", msg_key="", **kwargs):
        """
        Logs a success message.

        Args:
            prefix (str): The prefix to add before the message. Default is a space.
            msg_key (str): The key for the message to translate.
            **kwargs: Additional arguments for the translation.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(GREEN, f"{prefix} {msg}")

    def warning(self, prefix=" ", msg_key="", **kwargs):
        """
        Logs a warning message.

        Args:
            prefix (str): The prefix to add before the message. Default is a space.
            msg_key (str): The key for the message to translate.
            **kwargs: Additional arguments for the translation.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(WARN, f"{prefix} {msg}")

    def error(self, prefix=" ", msg_key="", **kwargs):
        """
        Logs an error message.

        Args:
            prefix (str): The prefix to add before the message. Default is a space.
            msg_key (str): The key for the message to translate.
            **kwargs: Additional arguments for the translation.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(RED, f"{prefix} {msg}")

    def debug(self, prefix=" ", msg_key="", **kwargs):
        """
        Logs a debug message.

        Args:
            prefix (str): The prefix to add before the message. Default is a space.
            msg_key (str): The key for the message to translate.
            **kwargs: Additional arguments for the translation.
        """
        msg = self.translate(msg_key, **kwargs)
        self._log(BLUE, f"{prefix} {msg}")
