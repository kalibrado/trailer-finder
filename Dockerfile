FROM python:3.11-alpine

WORKDIR /app


COPY requirements.txt ./requirements.txt

RUN apk update && apk add --no-cache ffmpeg \
      && pip install --upgrade pip \
      && pip install --no-cache-dir -r requirements.txt \
      && apk del --purge --no-cache \
      && rm -rf /var/cache/apk/* \
      && rm -rf /root/.cache/pip 

COPY ./config/ ./config
COPY ./modules/ ./modules
COPY ./locales/ ./locales
COPY ./main.py ./main.py


RUN rm -rf /usr/local/bin/pip /usr/local/bin/pip3

CMD ["python", "-u", "main.py"]
