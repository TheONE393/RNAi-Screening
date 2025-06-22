import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCHED_DIR = "Images"
VALID_EXTS = ('.jpg', '.jpeg', '.png', '.gif', '.webp')
DEBOUNCE_SECONDS = 5
last_event_time = 0
pending_lines = set()

class ImageHandler(FileSystemEventHandler):
    def process(self, event):
        global last_event_time
        if event.is_directory:
            return

        _, ext = os.path.splitext(event.src_path)
        if ext.lower() not in VALID_EXTS:
            return

        # Get line ID
        rel_path = os.path.relpath(event.src_path, WATCHED_DIR)
        parts = rel_path.split(os.sep)
        if len(parts) < 2:
            print("⚠️ Cannot determine line ID from path:", event.src_path)
            return

        line_id = parts[0]
        pending_lines.add(line_id)
        last_event_time = time.time()

    def on_created(self, event):
        self.process(event)

    def on_modified(self, event):
        self.process(event)

def run_update_scripts(line_id):
    print(f"🔄 Updating for line {line_id}")
    subprocess.run(["python", "auto_insert_images.py", line_id])
    subprocess.Popen(["python", "generate_pages.py", line_id])

def push_to_github():
    print("📤 Pushing changes to GitHub...")
    subprocess.run(["python", "auto_push_to_github.py"])

if __name__ == "__main__":
    print("🕹️ Initial run...")
    subprocess.run(["python", "auto_insert_images.py"])
    subprocess.Popen(["python", "generate_pages.py"])

    event_handler = ImageHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCHED_DIR, recursive=True)
    observer.start()

    print(f"👀 Watching {WATCHED_DIR}/")

    try:
        while True:
            time.sleep(1)
            now = time.time()
            if pending_lines and now - last_event_time > DEBOUNCE_SECONDS:
                for line_id in pending_lines.copy():
                    run_update_scripts(line_id)
                push_to_github()
                pending_lines.clear()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
