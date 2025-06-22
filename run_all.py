import subprocess
import threading
import time

def run_watch_and_generate():
    print("👀 Starting watch_and_generate.py...")
    subprocess.run(["python", "watch_and_generate.py"])

def run_upload_server():
    print("🚀 Starting upload_server.py...")
    subprocess.run(["python", "upload_server.py"])

if __name__ == "__main__":
    try:
        # Upload server (Flask)
        t1 = threading.Thread(target=run_upload_server)

        # Watchdog + Auto Git Push
        t2 = threading.Thread(target=run_watch_and_generate)

        # Start threads (do NOT daemonize)
        t1.start()
        t2.start()

        # Wait for threads to finish
        t1.join()
        t2.join()

    except KeyboardInterrupt:
        print("🛑 Received exit signal. Shutting down gracefully...")
