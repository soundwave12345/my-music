import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# === CONFIG ===
WATCH_DIR = "music"         # cartella da monitorare
SCRIPT_TO_RUN = "playlist_manager.py"  # nome del tuo script principale

class MusicHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        if event.src_path.lower().endswith(".flac"):
            print(f"Nuovo file rilevato: {event.src_path}")
            print("Eseguo script di aggiornamento...")
            subprocess.run(["python", SCRIPT_TO_RUN], check=False)

if __name__ == "__main__":
    observer = Observer()
    handler = MusicHandler()
    observer.schedule(handler, WATCH_DIR, recursive=True)
    observer.start()

    print(f"Monitoraggio avviato su: {WATCH_DIR}")


    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        print("Monitoraggio interrotto.")
    observer.join()
