# Smaller Alpine image
FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt && rm -rf ~/.cache/pip
COPY . /app
RUN ls /app/config
CMD ["python", "main.py"]