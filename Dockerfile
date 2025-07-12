FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y ffmpeg curl && \
    pip install --no-cache-dir flask gunicorn yt-dlp && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

EXPOSE 8080
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]
