import os
import json

images_folder = "Images"
valid_ext = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

for line in os.listdir(images_folder):
    line_folder = os.path.join(images_folder, line)
    if not os.path.isdir(line_folder):
        continue

    desc_path = os.path.join(line_folder, "descriptions.json")
    if os.path.exists(desc_path):
        print(f"✅ Found: {desc_path}")
        continue

    # Generate default descriptions
    entries = {}
    for img in os.listdir(line_folder):
        if os.path.splitext(img)[1].lower() in valid_ext:
            entries[img] = {
                "caption": os.path.splitext(img)[0],  # Use filename as default caption
                "description": ""
            }

    with open(desc_path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)

    print(f"📝 Created: {desc_path}")
