FROM python:3.11-alpine

WORKDIR /app

COPY requirements.txt .

RUN apk update && apk add --no-cache ffmpeg \
      && pip install --upgrade pip \
      && pip install --no-cache-dir -r requirements.txt \
      && apk del --purge --no-cache make gcc g++ \
      && rm -rf /var/cache/apk/* \
      && rm -rf /root/.cache/pip

COPY . .

RUN rm -f /usr/local/bin/pip /usr/local/bin/pip3

CMD ["python", "-u", "main.py"]
