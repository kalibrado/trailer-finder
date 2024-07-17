"""modules/exceptions.py"""


class ArrApiError(Exception):
    """Radarr/Sonarr api exceptions."""


class TranslatorError(Exception):
    """Translator module exceptions."""


class DurationError(Exception):
    """Invalid Duration exceptions."""


class DonwloadError(Exception):
    """Donwload exceptions."""


class FfmpegError(Exception):
    """Ffmpeg error exceptions."""


class FfmpegCommandMissing(Exception):
    """Ffmpeg command missing exceptions."""


class InsufficientDiskSpaceError(Exception):
    """Disk space exceptions."""
