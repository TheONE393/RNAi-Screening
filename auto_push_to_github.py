import subprocess
import datetime

# === Git Commands ===
try:
    # Stage all changes
    subprocess.run(["git", "add", "."], check=True)

    # Commit with timestamp
    commit_msg = f"Auto-update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    subprocess.run(["git", "commit", "-m", commit_msg], check=True)

    # Push to remote
    subprocess.run(["git", "push"], check=True)

    print("✅ Successfully pushed to GitHub.")
except subprocess.CalledProcessError as e:
    print(f"❌ Git error: {e}")
