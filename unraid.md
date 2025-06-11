# 🎬 Unraid Deployment Guide for Trailer Finder

This guide explains how to run **Trailer Finder** alongside **Radarr** and **Sonarr** on an Unraid server.  
You can either deploy it directly in a Docker container on Unraid, or run it from another machine on your network.

---

## 🗂 Table of Contents

- [🎬 Unraid Deployment Guide for Trailer Finder](#-unraid-deployment-guide-for-trailer-finder)
  - [🗂 Table of Contents](#-table-of-contents)
  - [✅ Requirements](#-requirements)
  - [🚀 Method 1 – Run in Docker on Unraid](#-method-1--run-in-docker-on-unraid)
    - [1. Place your config file](#1-place-your-config-file)
    - [2. Run the container](#2-run-the-container)
    - [Breakdown:](#breakdown)
    - [⚠️ Important – Path Consistency Between Containers](#️-important--path-consistency-between-containers)
  - [🖥️ Method 2 – Run on another machine](#️-method-2--run-on-another-machine)
    - [1. Clone the project](#1-clone-the-project)
    - [2. Create and configure `config.yaml`](#2-create-and-configure-configyaml)
    - [3. Run the app](#3-run-the-app)
  - [📂 Example config.yaml](#-example-configyaml)
  - [🌐 Network \& Volume Mapping](#-network--volume-mapping)
  - [✅ Final Notes](#-final-notes)
  - [🙋 Need Help?](#-need-help)

---

## ✅ Requirements

- Unraid server with Docker enabled.
- Radarr and/or Sonarr installed as containers.
- Your Trailer Finder `config.yaml` file.
- Radarr/Sonarr API keys.
- Media files accessible on the Unraid server or via SMB/NFS.
- Internet access to fetch trailers via TMDB and YouTube.

---

## 🚀 Method 1 – Run in Docker on Unraid

You can run Trailer Finder in a Docker container on the Unraid server itself.

### 1. Place your config file

Place your configuration file (`config.yaml`) on the Unraid system.  
For example, copy it to:

```
/mnt/user/appdata/trailer-finder/config/config.yaml
```

> 📌 **Important**: The container expects it at `/app/config/config.yaml`.

---

### 2. Run the container

Use this command in the Unraid terminal or add it to the Unraid Docker GUI:

```bash
docker run -d \
  --name trailer-finder \
  -v /mnt/user/appdata/trailer-finder/config:/app/config:ro \
  -v /mnt/user/media:/mnt/media \
  --network=host \
  ghcr.io/kalibrado/trailer-finder:latest
````

### Breakdown:

* `-v config:/app/config:ro`: mounts your config folder inside the container.
* `-v media:/mnt/media`: maps your media location (where trailers will be saved).
* `--network=host`: allows Trailer Finder to communicate with Radarr and Sonarr on localhost (`127.0.0.1`).

---

### ⚠️ Important – Path Consistency Between Containers

To work correctly, **Trailer Finder must see the exact same file paths** as Radarr and Sonarr do.

> For example:
> If Radarr shows a movie path as `/mnt/media/Movies/Inception (2010)`,
> then that **exact same path** must also exist inside the `trailer-finder` container.

If paths differ (e.g., Radarr uses `/data` but trailer-finder sees `/mnt/media`), the lookup will fail because the trailer-finder won’t find the file.

📌 To ensure this:

* Use the same volume mount in all containers (Radarr, Sonarr, trailer-finder).
* Match the **host path** to the **container path** for consistency.

Example setup across all containers:

| Volume | Host Path         | Container Path |
| ------ | ----------------- | -------------- |
| Media  | `/mnt/user/media` | `/mnt/media`   |

This way, Radarr, Sonarr, and trailer-finder all operate on the same visible paths.

---

## 🖥️ Method 2 – Run on another machine

You can also run Trailer Finder on any other device on the same LAN (e.g., PC, NAS, Raspberry Pi).

### 1. Clone the project

```bash
git clone https://github.com/kalibrado/trailer-finder.git
cd trailer-finder
pip install -r requirements.txt
```

### 2. Create and configure `config.yaml`

Make sure to set the correct IP addresses of Radarr and Sonarr in Unraid:

```yaml
# Configuration for Sonarr

# Sonarr host address
SONARR_HOST: "http://192.168.1.100:8989"

# Sonarr API key
SONARR_API: "your_SONARR_API_key"

# Configuration for Radarr

# Radarr host address
RADARR_HOST: "http://192.168.1.100:7878"

# Radarr API key
RADARR_API: "your_RADARR_API_key"
```

> Replace `192.168.1.100` with your Unraid server’s IP.

### 3. Run the app

```bash
python main.py
```

---

## 📂 Example config.yaml

```yaml
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
```

* If running on Unraid via Docker with `--network=host`, use `127.0.0.1`.
* If running externally, use the local IP of your Unraid box.

---

## 🌐 Network & Volume Mapping

| Component    | Host Path                                 | Container Path            | Purpose                                  |
| ------------ | ----------------------------------------- | ------------------------- | ---------------------------------------- |
| Config File  | `/mnt/user/appdata/trailer-finder/config` | `/app/config` (read-only) | Used to load `config.yaml`               |
| Media Folder | `/mnt/user/media`                         | `/mnt/media`               | Where trailers are downloaded            |
| Network      | `--network=host`                          | Host bridge               | Required for API access to Radarr/Sonarr |

---

## ✅ Final Notes

* Trailer Finder works seamlessly with Docker in Unraid as long as:

  * You mount the correct volumes.
  * You use `--network=host` if Radarr/Sonarr are on localhost.
* You can run it manually or schedule it via Unraid's User Scripts plugin or cron job.
* You can also create a Docker template XML if you want a GUI install option.

---

## 🙋 Need Help?

If you're unsure how to set up your config or volumes, feel free to open an issue or discussion on [GitHub](https://github.com/kalibrado/trailer-finder/issues). 🚀
