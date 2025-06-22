# watch_and_generate.py

import time
import subprocess
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_DIR = "Images"
valid_ext = ('.jpg', '.jpeg', '.png', '.gif', '.webp')

class ImageHandler(FileSystemEventHandler):
    def process(self, event):
        if event.is_directory:
            return

        ext = os.path.splitext(event.src_path)[1].lower()
        if ext not in valid_ext:
            return  # ❗ Ignore non-image files

        # Confirm file really exists (some intermediate tmp files may trigger event)
        if not os.path.exists(event.src_path):
            return

        # Determine line ID from path
        rel_path = os.path.relpath(event.src_path, WATCHED_DIR)
        parts = rel_path.split(os.sep)
        if len(parts) < 2:
            print("⚠️ Cannot determine line ID from path:", event.src_path)
            return

        line_id = parts[0]
        print(f"\n📸 Detected image change in line {line_id}")
        run_scripts_for_line(line_id)


    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

def run_scripts_for_line(line_id):
    print(f"⚙️ Updating HTML and image insertion for: {line_id}")

    subprocess.run(["python", "auto_insert_images.py", line_id])
    subprocess.run(["python", "generate_pages.py", line_id])

if __name__ == "__main__":
    print("🕹️ Initial scan of all folders...")
    subprocess.run(["python", "auto_insert_images.py"])
    subprocess.run(["python", "generate_pages.py"])

    print(f"👀 Watching for changes in: {WATCHED_DIR}/ (including subfolders)")

    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_DIR, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
