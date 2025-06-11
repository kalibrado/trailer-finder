# 🎬 Unraid Deployment Guide for Trailer Finder

This guide explains how to run **Trailer Finder** with **Radarr** and **Sonarr** on Unraid, either **within a Docker container** on Unraid or **from another machine** on the same network.

---

## 🔧 Pre-requisites

- Unraid server with Radarr & Sonarr installed via Docker.
- Access to Unraid Docker or terminal.
- Radarr/Sonarr API keys.
- `config.yaml` (or `config.sample.yaml`) in your repo.
- Docker or Python 3.10+ on host or network-accessible machine.

---

## Method 1 – Run Trailer Finder as a Docker container on Unraid

### 1. Setup shared directory for trailers

On Unraid web UI:  
- Go to **Shares**, create or use an existing share (e.g. `trailers` or your media folder).
- Note its mount path (e.g. `/mnt/user/media`).

### 2. Deploy Trailer Finder container

Use Docker CLI (in Unraid Terminal or at the Unraid server):

```bash
docker run -d \
  --name trailer-finder \
  -v /mnt/user/appdata/trailer-finder/config.yaml:/app/config/config.yaml:ro \
  -v /mnt/user/media:/mnt/media\
  --network=host \
  ghcr.io/kalibrado/trailer-finder:latest
````

* Adjust volume mounts to match your paths.
* `--network=host` allows `localhost` access to Radarr/Sonarr on Unraid.
* Your `config.yaml` file should reference URLs like `http://127.0.0.1:7878`.

---

## Method 2 – Run Trailer Finder on another machine

This could be a separate server, PC, or Pi on the same LAN.

### 1. Clone and install

```bash
git clone https://github.com/kalibrado/trailer-finder.git
cd trailer-finder
pip install -r requirements.txt
```

### 2. Configure `config.yaml`

Update `url:` fields with your Unraid server’s local IP, e.g.:

```yaml
# Configuration for Sonarr

# Sonarr host address
SONARR_HOST: "http://192.168.10.100:8989"

# Sonarr API key
SONARR_API: "your_SONARR_API_key"

# Configuration for Radarr

# Radarr host address
RADARR_HOST: "http://192.168.10.100:7878"

# Radarr API key
RADARR_API: "your_RADARR_API_key"

```

Ensure the downloading machine mounts or can write to `/mnt/media`.

### 3. Run Launcher

```bash
python main.py
```

---

## ⚙️ Volume & Networking Overview

| Use Case      | Path on Host      | Path in Container | Network Access              |
| ------------- | ----------------- | ----------------- | --------------------------- |
| Unraid Docker | `/mnt/user/media` | `/mnt/media`       | `localhost:7878`, `:8989`   |
| External Host | any local path    | `/mnt/media`       | `192.168.x.x:7878`, `:8989` |

* Important: `--network=host` allows container to “see” Radarr/Sonarr via `127.0.0.1`.
* Ensure correct `url:` in `config.yaml`.
* Map media share to `output_path`.

---

## ✅ Example `config.yaml`

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

---

## 💡 Optional: Unraid Docker Template

You can paste the above `docker run` command into a custom Docker template XML in Unraid, making the setup reusable via the Unraid UI.