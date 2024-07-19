"""
Module defining custom exceptions for handling errors in the application.

This module contains custom exception classes that are used throughout the application
to handle specific error conditions. Each exception class is designed to signal distinct
types of errors that may occur in different parts of the application, such as issues
related to API interactions, translation errors, file downloads, and logging configurations.

Custom exceptions are used to provide more informative and specific error messages,
improve error handling, and facilitate debugging by clearly identifying the nature
of the problems encountered.

Exception Classes:
    - **ArrApiError**: Raised for errors related to Radarr/Sonarr APIs, such as invalid API responses or failed API calls.
    - **TranslatorError**: Raised for errors in the Translator module, including translation failures or missing keys.
    - **DurationError**: Raised when an invalid duration is encountered, such as incorrect format or out-of-range values.
    - **DownloadError**: Raised for errors during the download process, including network failures or permission issues.
    - **FfmpegError**: Raised for errors related to Ffmpeg operations, such as processing errors or command execution problems.
    - **FfmpegCommandMissing**: Raised when a required Ffmpeg command is missing from the configuration or is unavailable.
    - **InsufficientDiskSpaceError**: Raised when there is insufficient disk space available for performing operations.
    - **InvalidLogSizeError**: Raised when the size of the log file specified in the configuration is invalid or out of range.
    - **InvalidLogCountError**: Raised when the number of log backup files specified in the configuration is invalid.
    - **InvalidLogLevelError**: Raised when the log level defined in the configuration is not among the recognized levels.

Usage:
    Import this module to access custom exception classes for handling specific error conditions
    in the application. These exceptions can be raised and caught in different parts of the
    codebase to manage error scenarios effectively and provide meaningful error messages.

Example:
    To use an exception from this module, you can do the following:

    .. code-block:: python

        from modules.exceptions import ArrApiError, DownloadError

        try:
            # Some code that might raise an ArrApiError
            pass
        except ArrApiError as e:
            print(f"API Error: {e}")

    In this example, the `ArrApiError` exception is used to handle errors related to API operations.
"""


class ArrApiError(Exception):
    """
    Exception raised for errors related to Radarr/Sonarr APIs.

    This exception is used to signal issues that occur while interacting with
    the Radarr or Sonarr APIs. It may be raised in cases where API responses
    are invalid, API calls fail, or other API-related errors are encountered.
    """

    pass


class TranslatorError(Exception):
    """
    Exception raised for errors in the Translator module.

    This exception is used to signal issues within the Translator module, such
    as failures in message translation, missing translation keys, or errors
    in the localization process.
    """

    pass


class DurationError(Exception):
    """
    Exception raised when an invalid duration is encountered.

    This exception is used to indicate that a provided duration is not valid.
    It may be raised if the duration format is incorrect or if the duration
    value is out of acceptable range.
    """

    pass


class DownloadError(Exception):
    """
    Exception raised for errors during the download process.

    This exception is used to indicate that an error occurred while attempting
    to download a file or resource. It can cover various issues such as network
    failures, corrupted files, or permission problems during the download process.
    """

    pass


class FfmpegError(Exception):
    """
    Exception raised for errors related to Ffmpeg operations.

    This exception is used to signal issues that occur while performing operations
    with Ffmpeg, such as video or audio processing errors, conversion failures,
    or command execution problems.
    """

    pass


class FfmpegCommandMissing(Exception):
    """
    Exception raised when a required Ffmpeg command is missing.

    This exception is used to indicate that a necessary Ffmpeg command is not
    specified in the configuration or is otherwise unavailable. It is raised
    when the absence of this command prevents proper execution of Ffmpeg tasks.
    """

    pass


class InsufficientDiskSpaceError(Exception):
    """
    Exception raised when there is insufficient disk space.

    This exception is used to indicate that there is not enough disk space available
    to perform a required operation, such as saving files or performing large downloads.
    It helps ensure that operations are not attempted when disk space constraints
    would cause failures.
    """

    pass


class InvalidLogSizeError(Exception):
    """
    Exception raised when the size of the defined logs in the config file is not valid.

    This exception is used to indicate that the specified log file size in the
    configuration file is invalid, either because it is not a positive integer
    or it does not meet the required constraints.
    """

    pass


class InvalidLogCountError(Exception):
    """
    Exception raised when the number of logs saved in the configuration file is not a valid format.

    This exception is used to signal that the configured number of log backup
    files is invalid, either because it is not a non-negative integer or it does
    not meet the required constraints.
    """

    pass


class InvalidLogLevelError(Exception):
    """
    Exception raised when the defined log level is not valid.

    This exception is used to indicate that the specified log level in the configuration
    is not valid. It may be raised if the log level is not among the recognized levels
    such as DEBUG, INFO, WARNING, ERROR, or CRITICAL.
    """

    pass
