# run_all.py
import subprocess

subprocess.Popen(["python", "upload_server.py"])
subprocess.Popen(["python", "watch_and_generate.py"])
