import os

lines_folder = "lines"
images_folder = "images"

# Supported image extensions
image_exts = ('.jpg', '.jpeg', '.png', '.gif')

for html_file in os.listdir(lines_folder):
    if not html_file.endswith(".html"):
        continue

    line_id = html_file.replace(".html", "")
    html_path = os.path.join(lines_folder, html_file)
    image_dir = os.path.join(images_folder, line_id)

    if not os.path.exists(image_dir):
        print(f"⚠️  No image folder for line {line_id}. Skipping...")
        continue

    # Get image file list
    image_files = [img for img in os.listdir(image_dir) if img.lower().endswith(image_exts)]
    if not image_files:
        print(f"ℹ️  No images in {image_dir}")
        continue

    # Create HTML for gallery
    image_html = '\n<div class="image-gallery">\n'
    for img in sorted(image_files):
        rel_path = f"../images/{line_id}/{img}"
        image_html += f'  <img src="{rel_path}" alt="{img}" style="max-width:100%; margin-bottom:1em;">\n'
    image_html += '</div>\n'

    # Read and update existing HTML file
    with open(html_path, "r", encoding="utf-8") as f:
        content = f.read()

    if image_html in content:
        print(f"✅ Already updated: {html_file}")
        continue

    if "</body>" in content:
        content = content.replace("</body>", image_html + "</body>")
    else:
        content += "\n" + image_html

    # Save updated HTML
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✅ Inserted {len(image_files)} image(s) into {html_file}")
