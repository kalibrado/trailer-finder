Custom Exceptions
=================
.. automodule:: modules.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

   Custom exceptions for Trailer Finder.

   This module defines custom exceptions that are used throughout the Trailer Finder application
   for handling specific error scenarios.

   Exceptions:
      - ArrApiError: Raised for errors related to Radarr/Sonarr APIs.
      - TranslatorError: Raised for errors in the Translator module.
      - DurationError: Raised when an invalid duration is encountered.
      - DownloadError: Raised for errors during the download process.
      - FfmpegError: Raised for errors related to Ffmpeg operations.
      - FfmpegCommandMissing: Raised when a required Ffmpeg command is missing.
      - InsufficientDiskSpaceError: Raised when there is insufficient disk space.

   Each exception provides a specific error context for different failure scenarios encountered
   during the execution of the application. These exceptions help in better error handling and
   providing meaningful error messages to users or administrators.