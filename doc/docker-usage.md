# Trailer Finder - Docker Usage

## Requirements

- Docker installed on your system.
- Docker Compose installed (optional but recommended).

## Using the Docker Image

The `ldfe/trailer-finder` Docker image simplifies setting up Trailer Finder.

### 1. Pull the Docker Image

```bash
docker pull ldfe/trailer-finder:latest
```

### 2. Run the Docker Container

```bash
docker run -d \
  --name=trailer-finder \
  -v /path/to/your/config.yaml:/app/config/config.yaml \
  -v /mnt/Media1:/mnt/Media1 \
  -v /mnt/Media2:/mnt/Media1 \
  ldfe/trailer-finder:latest
```

Replace paths as necessary.

## Using Docker Compose

To simplify the setup further, use Docker Compose.

### Docker Compose File: `docker-compose.yaml`

```yaml
version: "3"
services:
  trailer-finder:
    image: ldfe/trailer-finder:latest
    restart: always
    volumes:
      - ./config.yaml:/app/config/config.yaml
      - /mnt/Media1:/mnt/Media1
      - /mnt/Media2:/mnt/Media1
```

### Steps to Run with Docker Compose

1. **Create the Docker Compose File**

   Place `docker-compose.yaml` in your project directory.

2. **Prepare the Configuration File**

   Ensure `config.yaml` is in the same directory.

3. **Run Docker Compose**

```bash
docker-compose up -d
```

## Configuration

Edit `config.yaml` to customize Trailer Finder. 

### Sample `config.yaml`

Refer to the local usage document for detailed configuration options.

## Troubleshooting

- Verify paths in `docker-compose.yaml`.
- Ensure `config.yaml` is correctly formatted.
- Check Docker logs for errors.