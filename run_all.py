import subprocess
import threading
import time

def run_watch_and_generate():
    print("👀 Starting watch_and_generate.py...")
    subprocess.run(["python", "watch_and_generate.py"])

def run_auto_push_loop(interval=300):
    try:
        while True:
            print("🔄 Running auto_push_to_github.py...")
            subprocess.run(["python", "auto_push_to_github.py"])
            time.sleep(interval)
    except Exception as e:
        print(f"❌ Auto-push thread error: {e}")

def run_upload_server():
    print("🚀 Starting upload_server.py...")
    subprocess.run(["python", "upload_server.py"])

if __name__ == "__main__":
    try:
        t1 = threading.Thread(target=run_watch_and_generate)
        t2 = threading.Thread(target=run_auto_push_loop)
        t3 = threading.Thread(target=run_upload_server)

        # Do NOT mark them daemon
        t1.start()
        t2.start()
        t3.start()

        # Keep main alive until threads are done (they won’t be unless killed)
        t1.join()
        t2.join()
        t3.join()

    except KeyboardInterrupt:
        print("🛑 Received exit signal. Shutting down gracefully...")
