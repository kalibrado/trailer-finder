""" modules/logger.py """

from time import sleep
import sys
from modules.translator import Translator

# Console colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
WARN = "\033[0;33m"
WHITE = "\033[37m"


class Logger(Translator):
    def __init__(self, default_locale="en"):
        super().__init__(default_locale)

    def _log(self, color: str, msg: str):
        sys.stdout.write(f"{color} {msg} {RESET}")
        sys.stdout.write("\n")
        sys.stdout.flush()
        sleep(0.5)

    def info(self, prefix=" ", msg_key="", **kwargs):
        msg = self.translate(msg_key, **kwargs)
        self._log(BLUE, f"{prefix} {msg}")

    def success(self, prefix=" ", msg_key="", **kwargs):
        msg = self.translate(msg_key, **kwargs)
        self._log(GREEN, f"{prefix} {msg}")

    def warning(self, prefix=" ", msg_key="", **kwargs):
        msg = self.translate(msg_key, **kwargs)
        self._log(WARN, f"{prefix} {msg}")

    def error(self, prefix=" ", msg_key="", **kwargs):
        msg = self.translate(msg_key, **kwargs)
        self._log(RED, f"{prefix} {msg}")
