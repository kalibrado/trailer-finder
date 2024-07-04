# Smaller Alpine image
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN apk update && apk add --no-cache ffmpeg && pip install --upgrade pip && pip install -r requirements.txt && rm -rf ~/.cache/pip
COPY . /app
RUN ls /app/config
CMD ["python", "-u", "/app/main.py"]