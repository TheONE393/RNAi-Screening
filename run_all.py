import subprocess
import threading
import time
import os

# Determine base directory (where this script is located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def run_watch_and_generate():
    print("🔁 Starting watch_and_generate.py...")
    subprocess.run(["python", os.path.join(BASE_DIR, "watch_and_generate.py")])

def run_auto_push_loop(interval=3):
    try:
        while True:
            print("🔁 Running auto_push_to_github.py...")
            subprocess.run(["python", os.path.join(BASE_DIR, "auto_push_to_github.py")])
            time.sleep(interval)
    except Exception as e:
        print(f"❌ Auto-push thread error: {e}")

def run_upload_server():
    print("🔁 Starting upload_server.py...")
    subprocess.run(["python", os.path.join(BASE_DIR, "upload_server.py")])

if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=run_watch_and_generate)
        t2 = threading.Thread(target=run_auto_push_loop)
        t3 = threading.Thread(target=run_upload_server)

        t1.start()
        t2.start()
        t3.start()

        t1.join()
        t2.join()
        t3.join()

    except KeyboardInterrupt:
        print("🛑 Received exit signal. Shutting down gracefully...")
