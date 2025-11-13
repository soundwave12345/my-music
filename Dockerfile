FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY playlist_manager.py music_watcher.py get_classifica.py scheduler.py ./

RUN pip install --no-cache-dir mutagen watchdog requests schedule thefuzz

RUN mkdir -p /app/music /app/old

VOLUME ["/app/music"]
VOLUME ["/app/mancanti"]

CMD ["bash", "-c", "python scheduler.py & python music_watcher.py"]
