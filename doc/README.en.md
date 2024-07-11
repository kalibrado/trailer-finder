### Trailer Finder

### Description

Trailer Finder is a Python-based automation tool designed to search and download movie and TV show trailers using Radarr and Sonarr APIs. It interacts with TMDB (The Movie Database) to fetch trailer information and utilizes yt-dlp to download trailers from YouTube. The tool is configurable via a YAML file and supports various options such as trailer search keywords, maximum trailer duration, and output directory settings.

---

### Table of Contents

- [Trailer Finder](#trailer-finder)
- [Description](#description)
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
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [Docker](#docker)

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
     git clone https://github.com/yourusername/trailer-finder.git
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
# Sonarr configuration
sonarr_host: "http://localhost:8989"
sonarr_api: "your_sonarr_api_key"

# Radarr configuration
radarr_host: "http://localhost:7878"
radarr_api: "your_radarr_api_key"

# TMDB API key (The Movie Database)
tmdb_api: "your_tmdb_api_key"

# Output directory for trailers
dir_backdrops: "backdrops"

# Base URL for YouTube links
yt_link_base: "https://www.youtube.com/watch?v="

# YouTube authentication information (optional)
auth_yt_user: "your_youtube_username"
auth_yt_pass: "your_youtube_password"

# Settings for downloading with Youtube-DL
no_warnings: True
skip_intros: True
max_length: 200
thread_count: 4
buffer_size_ffmpeg: "1M"
filetype: "mkv"

# Sleep time between executions in hours
sleep_time: 6

# YouTube search keywords for trailers
yt_search_keywords: "official trailer"

# Limit download to one trailer per item
only_one_trailer: True

# Minimum free disk space required in GB
min_free_space_gb: 5

# Default language for translation
default_locale: en

# Default language for trailers
default_language_trailer: en-US

# Quiet mode, suppress some logs for yt_dlp and ffmpeg process
quiet_mode: False
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

---

### Error Handling

- **Exception Handling**:
  - Captures exceptions during API interactions, file operations, and execution of external tools.
  - Logs errors with detailed error messages and context information.

- **Logging**:
  - Logs errors, warnings, and informational messages to provide visibility into tool operation and encountered issues.

---

### Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add a feature'`).
4. Push your branch (`git push origin feature/your-feature`).
5. Create a new Pull Request.

---

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
   version: '3'
   services:
     trailer-finder:
       image: ldfe/trailer-finder:tagname
       container_name: trailer-finder-app
       restart: always
   ```

   Launch the service with Docker Compose:

   ```bash
   docker-compose up -d
   ```
