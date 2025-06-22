
import subprocess
import threading
import time
import os



def run_watch_and_generate():
    print("👀 Starting watch_and_generate.py...")
    subprocess.run(["python", "watch_and_generate.py"])

def run_auto_push_loop(interval=300):  # every 5 minutes
    while True:
        print("🔄 Running auto_push_to_github.py...")
        subprocess.run(["python", "auto_push_to_github.py"])
        time.sleep(interval)
def run_upload_server():
    print("🚀 Starting upload_server.py...")
    subprocess.run(["python", "upload_server.py"])

if __name__ == "__main__":
    # Start folder watch
    t1 = threading.Thread(target=run_watch_and_generate)
    t1.daemon = True
    t1.start()

    # Start Git auto-push
    t2 = threading.Thread(target=run_auto_push_loop)
    t2.daemon = True
    t2.start()

    # Start upload server
    t3 = threading.Thread(target=run_upload_server)
    t3.daemon = True
    t3.start()

    # Keep main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Exiting master automation script.")
