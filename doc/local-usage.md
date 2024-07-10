# Trailer Finder - Local Usage

## Requirements

- Python 3.7 or higher.
- Valid API keys for Sonarr, Radarr, and TMDB (The Movie Database).

## Getting Started

### 1. Clone the Repository

Clone the Trailer Finder repository to your local machine:

```bash
git clone https://github.com/yourusername/trailer-finder.git
cd trailer-finder
```

### 2. Set Up a Virtual Environment

Create a virtual environment to avoid conflicts with other Python packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 4. Create the Configuration File

Create a `config.yaml` file with your settings and API keys. Here's a sample:

```yaml
sonarr_host: "http://localhost:8989"
sonarr_api: "your_sonarr_api_key"
radarr_host: "http://localhost:7878"
radarr_api: "your_radarr_api_key"
tmdb_api: "your_tmdb_api_key"
dir_backdrops: "trailers"
yt_link_base: "https://www.youtube.com/watch?v="
auth_yt_user: "your_youtube_username"
auth_yt_pass: "your_youtube_password"
no_warnings: True
skip_intros: True
max_length: 200
thread_count: 4
buffer_size_ffmpeg: "1M"
filetype: "mkv"
sleep_time: 6  # Set in hours, or remove to disable loop
yt_search_keywords: "official trailer"
only_one_trailer: True
min_free_space_gb: 5
default_language: "en"
default_language_trailer: "en-US" # Use ISO language codes
```

### 5. Run the Application

Run Trailer Finder with:

```bash
python trailer_finder.py
```

### 6. Check the Output

The trailers will be saved in the directory specified in `dir_backdrops`.

## Advanced Usage

### Running in Different Languages

Specify the desired language in `config.yaml` using ISO language codes under `default_language` (e.g., "en" for English).

### Scheduling Trailer Finder

You can schedule Trailer Finder using a cron job. 

#### Example: Daily Execution

Add the following entry to your crontab to run Trailer Finder every day at 6 AM:

```bash
0 6 * * * /path/to/your/venv/bin/python /path/to/your/project/trailer_finder.py
```

#### Example: Startup Execution

Add the following entry to run Trailer Finder on system boot:

```bash
@reboot /path/to/your/venv/bin/python /path/to/your/project/trailer_finder.py
```

### Integration with Radarr and Sonarr

Ensure that `sonarr_host`, `sonarr_api`, `radarr_host`, and `radarr_api` are correctly set in your `config.yaml`.

## Troubleshooting

- **Dependencies Issue**: Ensure all packages are installed correctly.
- **API Errors**: Check your API keys.
- **File Paths**: Verify file paths in `config.yaml`.
- **Permissions**: Ensure you have permissions to write to the `dir_backdrops`.
