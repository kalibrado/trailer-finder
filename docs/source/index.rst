Trailer Finder Documentation
============================

Welcome to the Trailer Finder documentation. Trailer Finder is a versatile automation tool designed to simplify the process of searching and downloading movie and TV show trailers. Built with Python, it integrates with Radarr and Sonarr APIs and uses TMDB (The Movie Database) for trailer information and yt-dlp for downloading from YouTube.

This guide will help you understand how to set up, configure, and use Trailer Finder effectively, whether you are running it manually or using Docker for containerized deployment.

Features
--------

- **Automated Trailer Downloads**: Automatically fetch trailers using specific keywords and API integrations.
- **Customizable Configuration**: Adjust settings such as search keywords, download criteria, and output directories according to your preferences.
- **Multilingual Support**: Select your preferred language for trailers and interface logs.
- **Error Handling**: Robust management of errors during API interactions and downloads.
- **Radarr and Sonarr Integration**: Seamless integration with Radarr and Sonarr for enhanced trailer management.
- **Docker Support**: Run Trailer Finder in isolated environments using Docker or Docker Compose.

Documentation Overview
----------------------

.. toctree::
      :maxdepth: 2
      :caption: Contents:

      usage
      configuration
      main
      modules

Indices and tables
==================

* :ref:`search`
* :ref:`genindex`
* :ref:`modindex`
