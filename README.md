
# Trailer Finder
[![Semgrep](https://github.com/kalibrado/trailer-finder/actions/workflows/semgrep.yml/badge.svg)](https://github.com/kalibrado/trailer-finder/actions/workflows/semgrep.yml)
[![Dependabot Updates](https://github.com/kalibrado/trailer-finder/actions/workflows/dependabot/dependabot-updates/badge.svg)](https://github.com/kalibrado/trailer-finder/actions/workflows/dependabot/dependabot-updates)
[![CodeQL](https://github.com/kalibrado/trailer-finder/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/kalibrado/trailer-finder/actions/workflows/github-code-scanning/codeql)


[!["Buy Me A Beer"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/leonardofod)

## Introduction

Trailer Finder is a versatile automation tool designed to streamline the process of searching and downloading movie and TV show trailers. Built on Python, it integrates seamlessly with Radarr and Sonarr APIs, leveraging TMDB (The Movie Database) for trailer information and yt-dlp for YouTube trailer downloads. Whether you're a movie enthusiast or managing a media library, Trailer Finder offers configurable options to enhance your trailer collection effortlessly.

---

## Key Features

- **Automated Trailer Downloads**: Fetch trailers automatically using keywords and API integrations.
- **Customizable Configuration**: Tailor settings such as trailer search keywords, download criteria, and output directories.
- **Multilingual Support**: Choose your preferred language for trailer downloads and interface logs.
- **Error Handling**: Robust error management ensures reliability during API interactions and downloads.
- **Integration with Radarr and Sonarr**: Seamlessly integrates with these platforms for enhanced trailer management.
- **Docker Support**: Run in isolated environments using Docker or Docker Compose.

---

## Documentation

### Table of Contents

- [Trailer Finder](#trailer-finder)
  - [Introduction](#introduction)
  - [Key Features](#key-features)
  - [Documentation](#documentation)
    - [Table of Contents](#table-of-contents)
    - [Installation](#installation)
    - [Usage](#usage)
    - [Configuration](#configuration)
    - [Module Overview](#module-overview)
      - [1. **Logger Module**](#1-logger-module)
      - [2. **Radarr Module**](#2-radarr-module)
      - [3. **Sonarr Module**](#3-sonarr-module)
      - [4. **Translator Module**](#4-translator-module)
      - [5. **Utils Module**](#5-utils-module)
      - [6. **YoutubeDL Module**](#6-youtubedl-module)
    - [Error Handling](#error-handling)
    - [Contributing](./CONTRIBUTING.md#contributing)
      - [Ways to Contribute](./CONTRIBUTING.md#ways-to-contribute)
      - [Getting Started](./CONTRIBUTING.md#getting-started)
        - [1. Fork the Repository](./CONTRIBUTING.md#1-fork-the-repository)
        - [2. Clone the Repository](./CONTRIBUTING.md#2-clone-the-repository)
        - [3. Create a New Branch](./CONTRIBUTING.md#3-create-a-new-branch)
        - [4. Make Changes](./CONTRIBUTING.md#4-make-changes)
        - [5. Test Your Changes](./CONTRIBUTING.md#5-test-your-changes)
        - [6. Commit Your Changes](./CONTRIBUTING.md#6-commit-your-changes)
        - [7. Push Your Changes](./CONTRIBUTING.md#7-push-your-changes)
        - [8. Create a Pull Request](./CONTRIBUTING.md#8-create-a-pull-request)
        - [9. Describe Your Pull Request](./CONTRIBUTING.md#9-describe-your-pull-request)
        - [10. Review and Discuss](./CONTRIBUTING.md#10-review-and-discuss)
        - [11. Merge Your Pull Request](./CONTRIBUTING.md#11-merge-your-pull-request)
      - [Code Style](#code-style)
      - [Report Issues](#report-issues)
      - [Acknowledgements](#acknowledgements)
    - [Docker](#docker)
  - [Troubleshooting](#troubleshooting)
  - [License](#license)

---

### Installation

To run Trailer Finder without Docker, make sure you have the following prerequisites installed on your system:

1. **Prerequisites**:
   - Python 3.7 or higher
   - `pip` (Python package management tool)
   - API keys for TMDB, Radarr, and Sonarr

2. **Installation Steps**:
   - Clone the GitHub repository:
     ```bash
     git clone https://github.com/kalibrado/trailer-finder.git
     cd trailer-finder
     ```

   - Install Python dependencies:
     ```bash
     pip install -r requirements.txt
     ```

3. **Configuration**:
   - Rename `config.sample.yaml` to `config.yaml`.
   - Configure API keys for TMDB, Radarr, and Sonarr along with other necessary settings in `config.yaml`.

---

### Usage

To run Trailer Finder after installation and configuration:

1. **Running the tool**:
   ```bash
   python main.py
   ```

2. **Stopping the tool**:
   - Use `Ctrl + C` in the console to stop execution.

3. **Logs**:
   - Logs are displayed in the console and can be redirected to log files if needed.

---

### Configuration

Trailer Finder's configuration is managed using a `config.yaml` file located in the `config` directory. Here's an example structure of the configuration file:

```yaml
# General Application Settings

# Key to use for movie/tv show title from *arr: title, originalTitle, sortTitle, cleanTitle
APP_USE_TITLE: "originalTitle"

# Limit to one trailer per item; last trailer is downloaded
APP_ONLY_ONE_TRAILER: true

# Time to wait between executions, in hours
APP_SLEEP_TIME: 6

# Minimum required free disk space in GB
APP_FREE_SPACE_GB: 5

# Default language for translation (e.g., en for English)
APP_TRANSLATE: en

# Quiet mode flag, suppresses some logs for yt_dlp and ffmpeg process
APP_QUIET_MODE: false

# Default directory for trailers; e.g., /path/of/radarr or sonarr/Name/backdrops/
APP_DEFAULT_DIR: "backdrops"

# Set this if you want to save trailers in a specific path
APP_CUSTOM_PATH: ""

# Custom name for TV show trailers (valid if APP_CUSTOM_PATH is set)
APP_CUSTOM_NAME_SHOW: "TV Show Trailer"

# Custom name for movie trailers (valid if APP_CUSTOM_PATH is set)
APP_CUSTOM_NAME_MOVIE: "Movies Trailers"

# Configuration for Sonarr

# Sonarr host address
SONARR_HOST: "http://localhost:8989"

# Sonarr API key
SONARR_API: "your_SONARR_API_key"

# Configuration for Radarr

# Radarr host address
RADARR_HOST: "http://localhost:7878"

# Radarr API key
RADARR_API: "your_RADARR_API_key"

# TMDB API Configuration (The Movie Database)

# TMDB API key
TMDB_API_KEY: "your_TMDB_API_KEY"

# Type of media to separate by '|' (e.g., "Trailer|Featurette|Clip")
TMDB_TYPE_ITEM: "Trailer"

# Only fetch official trailers
TMDB_OFFICIAL: true

# Default size (pixels) for trailers
TMDB_SIZE: 1080

# Only accept trailers from YouTube as a source
TMDB_SOURCE: "YouTube"

# Default language for trailers (e.g., en-US for English)
TMDB_LANGUAGE_TRAILER: en-US

# Settings for downloading with Youtube-DL

# Base URL for YouTube links
YT_DLP_BASE_URL: "https://www.youtube.com/watch?v="

# YouTube username for authentication
YT_DLP_AUTH_USER: "your_youtube_username"

# YouTube password for authentication
YT_DLP_AUTH_PASS: "your_youtube_password"

# Disable warnings
YT_DLP_NO_WARNINGS: true

# Skip video intros
YT_DLP_SKIP_INTROS: true

# Maximum acceptable video duration in seconds
YT_DLP_MAX_LENGTH: 200

# Base keyword for general official trailers
YT_DLP_SEARCH_KEYWORD: "official trailer"

# Keyword template for searching season-specific trailers
YT_DLP_SEARCH_KEYWORD_SEASON: "{show} Season {season_number}"

# Comment:
# YT_DLP_SEARCH_KEYWORD_SEASON will be concatenated with YT_DLP_SEARCH_KEYWORD
# to search for official season trailers on YouTube.
# For example, to search for the official trailer of Season 3 of the show "Stranger Things",
# the final search query will be "Stranger Things Season 3 official trailer".

# Set this for waiting time between yt_dlp requests
YT_DLP_INTERVAL_RESQUESTS: 0

# Preferred format for downloading videos
YT_DLP_FORMAT: "bestvideo+bestaudio"

# Segments to remove from trailers using yt_dlp
YT_DLP_SPONSORS_BLOCK:
  - "sponsor"
  - "intro"
  - "outro"
  - "selfpromo"
  - "preview"
  - "filler"
  - "interaction"

# Settings for ffmpeg

# Number of threads for processing
FFMPEG_THREAD_COUNT: 4

# Buffer size for FFMPEG
FFMPEG_BUFFER_SIZE: "1M"

# Output file type for trailers
FFMPEG_FILE_TYPE: "mkv"

# Template for FFMPEG command used for processing videos
# WARNING: Modify this template with caution. Changes may impact script functionality.
FFMPEG_COMMAND_TEMPLATE: "ffmpeg -i '{path}' -threads {thread} -c:v copy -c:a aac -af volume=-7dB -bufsize {buffer} -preset slow -y '{path_file}'"

```

---

### Module Overview

#### 1. **Logger Module**

- Handles logging messages with various severity levels (info, success, warning, error, debug).
- Supports multilingual logging using translation files.
- Provides colored output in the console for clarity.

#### 2. **Radarr Module**

- Interacts with the Radarr API to search and download movie trailers.
- Checks for trailer existence and downloads new trailers based on configuration settings.
- Manages directory management and verifies available space before initiating downloads.

#### 3. **Sonarr Module**

- Interacts with the Sonarr API to search and download TV show trailers.
- Manages trailer downloads at the episode level and ensures sufficient disk space before starting downloads.

#### 4. **Translator Module**

- Provides translation capabilities using YAML files stored in the `locales` directory.
- Supports dynamic message formatting based on translation keys.

#### 5. **Utils Module**

- Contains utility functions for various tasks such as disk space checking, trailer extraction from TMDB, and trailer downloading using yt-dlp.
- Integrates ffmpeg for post-processing downloaded trailers and ensures trailers meet specified duration criteria.

#### 6. **YoutubeDL Module**

- Handles downloading trailers from YouTube using yt-dlp.
- Supports various download formats and configuration options.
- Integrates logging functions to track download progress and errors.

---

### Error Handling

- **Exception Handling**:
  - Captures exceptions during API interactions, file operations, and execution of external tools.
  - Logs errors with detailed error messages and context information.

- **Logging**:
  - Logs errors, warnings, and informational messages to provide visibility into tool operation and encountered issues.

---


#####

 2. Clone the Repository

Clone your fork of the repository to your local machine:

```bash
git clone https://github.com/kalibrado/trailer-finder.git
cd trailer-finder
```

##### 3. Create a New Branch

Create a new branch for your contribution:

```bash
git checkout -b feature/your-feature
```

##### 4. Make Changes

Make your changes or additions to the codebase. Ensure your changes adhere to the coding style and guidelines used in the project.

##### 5. Test Your Changes

Test your changes thoroughly to ensure they work as expected. If you've added new features or fixed bugs, write tests to cover your code.

##### 6. Commit Your Changes

Once you are satisfied with your changes, commit them with a clear and descriptive commit message:

```bash
git commit -am 'Add feature/improvement'
```

##### 7. Push Your Changes

Push your changes to your forked repository on GitHub:

```bash
git push origin feature/your-feature
```

##### 8. Create a Pull Request

Go to the GitHub repository page of Trailer Finder. You should see a prompt to create a pull request for the branch you just pushed. Click on "Compare & pull request" to initiate the pull request.

##### 9. Describe Your Pull Request

Provide a clear description of your changes in the pull request. Include any relevant details about the changes made and why they are beneficial.

##### 10. Review and Discuss

Collaborate with maintainers and contributors through code reviews and discussions. Be responsive to feedback and be prepared to make further changes if needed.

##### 11. Merge Your Pull Request

Once your pull request is approved and all discussions are resolved, a project maintainer will merge your changes into the main branch.

#### Code Style

Follow the existing code style and conventions used in the project. This includes:

- Python: PEP 8 style guide
- Documentation: Use Markdown (.md) format with clear and concise explanations

#### Report Issues

If you encounter bugs, issues, or have suggestions for improvements, please [open an issue](https://github.com/kalibrado/trailer-finder/issues).

#### Acknowledgements

We appreciate all contributions to Trailer Finder, big or small! Thank you for helping to make this project better.

### Docker

Use Docker to run Trailer Finder in an isolated environment:

1. **Using Docker**

   Use your custom Docker image `ldfe/trailer-finder:tagname`:

   ```bash
   docker pull ldfe/trailer-finder:tagname
   docker run -d --name trailer-finder-app ldfe/trailer-finder:tagname
   ```

2. **Using Docker Compose**

   Use Docker Compose to manage Trailer Finder deployment with dependencies:

   Create a `docker-compose.yml` file:

   ```yaml
        version: "3"
        services:
          trailer-finder:
            image: ldfe/trailer-finder:latest
            restart: always
            security_opt:
              - no-new-privileges:true
            volumes:
              - ./config.yaml:./config/config.yaml # Where the config file will be located
              # the access path must correspond to those of radarr and sonarr
              - /mnt/Media1:/mnt/Media1 # media folder 1
              - /mnt/Media2:/mnt/Media1 # media folder 1
   ```

   Launch the service with Docker Compose:

   ```bash
   docker-compose up -d
   ```



---

## Troubleshooting

If you encounter issues, refer to the troubleshooting section in the documentation or [open an issue](https://github.com/kalibrado/trailer-finder/issues).

---

## License
 This project is licensed under the [MIT License](./LICENSE).


