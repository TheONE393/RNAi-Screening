# watch_and_generate.py

import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_DIR = "images"

class ImageHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            print(f"\n📸 New image detected: {event.src_path}")
            run_scripts()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
            print(f"\n✏️ Image modified: {event.src_path}")
            run_scripts()

def run_scripts():
    print("⚙️ Running auto_insert_images.py...")
    subprocess.run(["python", "auto_insert_images.py"])

    print("🚀 Running generate_pages.py...")
    subprocess.run(["python", "generate_pages.py"])

if __name__ == "__main__":
    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_DIR, recursive=True)
    observer.start()

    print(f"👀 Watching for changes in: {WATCHED_DIR}/ (including subfolders)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
