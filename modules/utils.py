""" modules/utils.py """

import os
import shutil
import subprocess
from time import sleep
from logging import getLogger, basicConfig, INFO
import re
import requests
import yaml
import yt_dlp
import urllib3
from modules.translator import Translator

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logs
basicConfig(level=INFO)
logger = getLogger(__name__)

# Console colors
RESET = "\033[0m"
RED = "\033[31m"
GREEN = "\033[32m"
BLUE = "\033[34m"
WHITE = "\033[37m"

# Load configuration
with open("config/config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# Initialize Translator with configuration parameters
translator = Translator(default_locale=config["default_locale"])


def replace_slash_backslash(text):
    """
    Replace forward slashes and backward slashes with spaces.
    Replace multiple spaces with a single space.

    :param text: Input text containing slashes
    :return: Text with replaced slashes and spaces
    """
    text = re.sub(r"[\\/]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def log(color, prefix, msg_key, **kwargs):
    """
    Logging function with colored output for better visibility.

    :param color: Color of the message
    :param prefix: Prefix to identify the log source
    :param msg_key: Key of the message to translate
    :param kwargs: Additional keyword arguments for message formatting
    """
    msg = translator.translate(msg_key, **kwargs)
    print(f"{color}{prefix}: {msg}\033[0m")
    sleep(1)


def trailer_pull(tmdb_id, item_type, parent_mode=False):
    """
    Retrieve trailer information from TMDB API.

    :param tmdb_id: TMDB ID of the movie or TV show
    :param item_type: Type of item ('movie' or 'tv')
    :param parent_mode: Flag for parent mode retrieval (TV)
    :return: List of cleaned trailer information
    """
    log(
        WHITE,
        "\t -> GET",
        "Getting information about {tmdb_id} {item_type}",
        tmdb_id=tmdb_id,
        item_type=item_type,
    )
    base_link = "api.themoviedb.org/3"
    api_key = config["tmdb_api"]
    url = f"https://{base_link}/{item_type}/{tmdb_id}/videos"
    if parent_mode:
        url = f"https://{base_link}/find/{tmdb_id}?external_source=imdb_id"

    headers = {"accept": "application/json"}
    response = requests.get(
        url,
        params={
            "api_key": api_key,
            "language": config["default_language_trailer"],
            "include_video_language": config["default_language_trailer"].split("-")[0],
        },
        headers=headers,
        timeout=10,
        verify=False,
    )
    response.raise_for_status()

    raw_trailers = response.json()
    clean_trailers = raw_trailers.get("tv_results" if parent_mode else "results", [])

    trailers = []
    for trailer in clean_trailers:
        if trailer.get("type") == "Trailer" and trailer.get("site") == "YouTube":
            trailer["yt_link"] = config["yt_link_base"] + trailer["key"]
            trailer["name"] = replace_slash_backslash(trailer["name"])
            trailers.append(trailer)

    return trailers


def post_process(cache_path, files, item_path):
    """
    Post-processing function for downloaded files using FFMPEG.

    :param cache_path: Path to downloaded files cache
    :param files: List of downloaded files
    :param item_path: Path to the item's directory
    """
    log(
        WHITE,
        "\t -> POST PROCESS",
        "Create '{path}' folder",
        path=f"{item_path}/{config['output_dirs']}",
    )
    output_path = os.path.join(item_path, config["output_dirs"])
    os.makedirs(output_path, exist_ok=True)

    for file in files:
        filename = os.path.splitext(os.path.basename(file))[0]
        filetype = config["filetype"]
        cmd = [
            "ffmpeg",
            "-i",
            f"{cache_path}/{file}",
            "-threads",
            str(config["thread_count"]),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-af",
            "volume=-7dB",
            "-bufsize",
            config["buffer_size_ffmpeg"],
            "-preset",
            "slow",
            "-y",
            f"{output_path}/{filename}.{filetype}",
        ]
        log(WHITE, "\t -> FFMPEG", "{cmd}", cmd=" ".join(cmd))

        with open(os.devnull, "wb") as output:
            subprocess.run(cmd, stdout=output, stderr=output, stdin=output, check=False)


def yt_dlp_process(link, ytdl_opts):
    """
    Download trailer using yt-dlp.

    :param link: Trailer link information
    :param ytdl_opts: Options for yt-dlp
    """
    ydl = yt_dlp.YoutubeDL(ytdl_opts)
    try:
        log(
            WHITE,
            "\t -> DOWNLOAD",
            "Downloading {title} trailer from {link}",
            title=link["name"],
            link=link["yt_link"],
        )
        ydl.download([link["yt_link"]])
    except yt_dlp.DownloadError as e:
        log(
            RED,
            "\t -> DOWNLOAD",
            "Failed to download from {link}: {error}",
            link=link["name"],
            error=e,
        )
    except ValueError as e:
        log(
            RED,
            "\t -> DOWNLOAD",
            "Invalid duration for {link}: {error}",
            link=link["name"],
            error=e,
        )


def trailer_download(links, item):
    """
    Download trailers from YouTube.

    :param links: List of YouTube trailer links
    :param item: Metadata of the item (movie or TV show)
    """
    cache_path = f'cache/{item["title"]}'
    os.makedirs(cache_path, exist_ok=True)

    def dl_progress(d):
        if d["status"] == "finished":
            log(GREEN, "\t -> DOWNLOAD", "Trailer downloaded.")
        elif d["status"] == "error":
            log(RED, "\t -> DOWNLOAD", "Trailer download failed.")

    ytdl_opts = {
        "progress_hooks": [dl_progress],
        "format": "bestvideo+bestaudio",
        "username": config["auth_yt_user"],
        "password": config["auth_yt_pass"],
        "no_warnings": config["no_warnings"],
        "outtmpl": f'{cache_path}/{item["sortTitle"]}',
        "quiet": True,
    }

    if config["skip_intros"]:
        ytdl_opts["postprocessors"] = [
            {"key": "SponsorBlock"},
            {
                "key": "ModifyChapters",
                "remove_sponsor_segments": [
                    "sponsor",
                    "intro",
                    "outro",
                    "selfpromo",
                    "preview",
                    "filler",
                    "interaction",
                ],
            },
        ]

    def check_duration(link, **info):
        duration = info.get("duration")
        max_length = config["max_length"]
        if duration and (int(duration) > int(max_length)):
            raise ValueError(
                "Invalid duration for {link}: {error}".format(
                    link=link["name"], error=f"{duration}s"
                )
            )

    if config["only_one_trailer"]:
        if config["max_length"]:
            ytdl_opts["match_filter"] = lambda info: check_duration(links[0], **info)
        ytdl_opts["outtmpl"] = f"{cache_path}/{links[0]['name']}"
        yt_dlp_process(links[0], ytdl_opts)
    else:
        for link in links:
            if config["max_length"]:
                ytdl_opts["match_filter"] = lambda info: check_duration(link, **info)
            ytdl_opts["outtmpl"] = f"{cache_path}/{link['name']}"
            yt_dlp_process(link, ytdl_opts)

    if os.path.exists(cache_path):
        files = os.listdir(cache_path)
        post_process(cache_path, files, item["path"])
        shutil.rmtree(cache_path)
    else:
        log(RED, "\t -> DOWNLOAD", "No cache folder for {title}", title=item["title"])


def check_space(path):
    """
    Check available disk space at the given path.

    :param path: Path to check for available disk space
    :return: True if disk space is sufficient, False otherwise
    """
    min_free_gb = config.get(
        "min_free_space_gb", 5
    )  # Minimum free space required in GB
    _, _, free = shutil.disk_usage(path)
    free_gb = free / (1024**3)  # Convert bytes to GB
    if free_gb < min_free_gb:
        log(
            RED,
            "DISK SPACE",
            "Insufficient disk space in {path}. Only {free_gb:.2f} GB free.",
            path=path,
            free_gb=free_gb,
        )
        return False
    return True


def check_existing_trailer(trailers, existing_trailers):
    """
    Check if trailers already exist for the given movie or TV show.

    :param trailers: List of trailers to check
    :param existing_trailers: List of existing trailers
    :return: List of trailers that need to be downloaded
    """
    new_download = []
    for trailer in trailers:
        if trailer["name"] not in existing_trailers:
            new_download.append(trailer)
    return new_download
