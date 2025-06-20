import os

# Read line IDs from text file
with open("text.txt", "r", encoding="utf-8") as f:
    line_ids = [line.strip() for line in f if line.strip()]

# Base folder where subfolders will be created
images_base = "images"
os.makedirs(images_base, exist_ok=True)

# Create subfolders
for line_id in line_ids:
    folder_path = os.path.join(images_base, line_id)
    os.makedirs(folder_path, exist_ok=True)
    print(f"📁 Created folder: {folder_path}")
