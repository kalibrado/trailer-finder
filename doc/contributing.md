# Trailer Finder - Contributing

## Directory Structure

```plaintext
trailer-finder/
│
├── cache/                  # Directory for storing cached trailers.
│
├── config/
│   ├── example.config.yaml # Example configuration file.
│   └── config.yaml         # User-modified configuration file.
│
├── docker/
│   ├── Dockerfile          # Dockerfile for building the application.
│   └── docker-compose.yml  # Docker Compose configuration.
│
├── locales/                # Directory for storing locale-specific JSON files.
│   ├── de.json
│   ├── en.json
│   ├── es.json
│   ├── fr.json
│   └── pt.json
│
├── modules/                # Directory for the main application modules.
│   ├── __init__.py
│   ├── radarr.py           # Module for interacting with Radarr API.
│   ├── sonarr.py           # Module for interacting with Sonarr API.
│   ├── translator.py       # Module for managing translations.
│   └── utils.py            # Utility functions.
│
├── README.md               # Main README with links to detailed documents.
│
├── doc/
│   ├── local-usage.md      # Detailed instructions for local usage.
│   ├── docker-usage.md     # Detailed instructions for Docker usage.
│   └── contributing.md     # Contribution guidelines and module descriptions.
│
└── requirements.txt        # List of dependencies.
```

## Modules Description

### `radarr.py`

This module interacts with the Radarr API to find and download trailers for movies.

### `sonarr.py`

This module interacts with the Sonarr API to find and download trailers for TV series.

### `translator.py`

Handles translations based on locale-specific JSON files.

### `utils.py`

Contains utility functions for logging, checking disk space, downloading trailers, and post-processing using `ffmpeg` and `yt-dlp`.

## How to Contribute

1. **Create a New Branch**

```bash
git checkout -b feature-branch-name
```

2. **Make Your Changes**

Commit changes with a meaningful message:

```bash
git commit -m 'Feature description'
```

3. **Push to the Branch**

```bash
git push origin feature-branch-name
```

4. **Submit a Pull Request**

Submit a pull request on GitHub.