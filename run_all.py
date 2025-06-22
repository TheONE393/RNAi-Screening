import subprocess
import time
import signal
import sys

# Keep references to subprocesses
processes = []

def run_script(script_name):
    print(f"🔁 Starting {script_name}...")
    process = subprocess.Popen(["python", script_name])
    processes.append(process)

def terminate_all():
    print("\n🛑 Terminating all subprocesses...")
    for proc in processes:
        if proc.poll() is None:  # Still running
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
    print("✅ All subprocesses terminated. Exiting cleanly.")
    sys.exit(0)

if __name__ == "__main__":
    try:
        run_script("upload_server.py")
        time.sleep(1)  # Let Flask start
        run_script("watch_and_generate.py")

        # Keep main alive
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        terminate_all()
