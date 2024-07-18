class ArrApiError(Exception):
    """Exception raised for errors related to Radarr/Sonarr APIs."""

    pass


class TranslatorError(Exception):
    """Exception raised for errors in the Translator module."""

    pass


class DurationError(Exception):
    """Exception raised when an invalid duration is encountered."""

    pass


class DownloadError(Exception):
    """Exception raised for errors during the download process."""

    pass


class FfmpegError(Exception):
    """Exception raised for errors related to Ffmpeg operations."""

    pass


class FfmpegCommandMissing(Exception):
    """Exception raised when a required Ffmpeg command is missing."""

    pass


class InsufficientDiskSpaceError(Exception):
    """Exception raised when there is insufficient disk space."""

    pass
