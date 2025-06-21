import os

# === CONFIGURATION ===
lines_folder = "lines"
images_folder = "Images"
filenames_path = "filenames.txt"
valid_ext = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

# === Load RNAi Line IDs ===
with open(filenames_path, "r", encoding="utf-8") as f:
    line_ids = [line.strip() for line in f if line.strip()]

# === Ensure all image folders exist ===
for line in line_ids:
    folder_path = os.path.join(images_folder, line)
    os.makedirs(folder_path, exist_ok=True)
    if not os.listdir(folder_path):
        with open(os.path.join(folder_path, ".gitkeep"), "w") as f:
            pass

# === HTML Page Template ===
page_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>RNAi Line {line}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="../style.css">
  <link href="https://cdn.jsdelivr.net/npm/glightbox/dist/css/glightbox.min.css" rel="stylesheet">
</head>
<body>

<!-- Page content remains the same as before -->
<div class="content">
  <h1 class="page-title">RNAi Line {line}</h1>
  <div class="image-gallery">
    {image_tags}
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/glightbox/dist/js/glightbox.min.js"></script>
<script>
  const lightbox = GLightbox({{
    selector: '.glightbox'
  }});
</script>
</body>
</html>
"""

# === Generate Each Line Page ===
os.makedirs(lines_folder, exist_ok=True)

for line in line_ids:
    image_folder = os.path.join(images_folder, line)
    images = [img for img in sorted(os.listdir(image_folder)) 
             if os.path.splitext(img)[1].lower() in valid_ext] if os.path.exists(image_folder) else []

    image_tags = "\n".join([
        f'''<div class="img-wrapper">
            <div class="loader-container">
                <img class="fly-loader" src="../assets/fly-loader.gif" alt="Loading...">
            </div>
            <a href="../Images/{line}/{img}" class="glightbox" data-gallery="gallery-{line}">
                <img src="../Images/{line}/{img}" 
                     alt="{os.path.splitext(img)[0]}" 
                     loading="lazy"
                     onload="this.style.opacity=1; this.previousElementSibling.style.display='none';">
            </a>
        </div>'''
        for img in images
    ])

    html_content = page_template.format(line=line, image_tags=image_tags)
    
    output_path = os.path.join(lines_folder, f"{line}.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated: {output_path}")

# === Generate index.html ===
index_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>RNAi Screening Index</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1 class="page-title">RNAi Line Navigator</h1>
  <div class="search-box">
    <input type="text" id="indexSearch" placeholder="Search for a line...">
  </div>
  <div class="index-container">
    <div class="index-table" id="indexTable">
      {line_rows}
    </div>
  </div>

<script>
  const searchInput = document.getElementById('indexSearch');
  const table = document.getElementById('indexTable');
  searchInput.addEventListener('input', () => {{
    const term = searchInput.value.toLowerCase();
    const rows = table.querySelectorAll('.index-row');
    rows.forEach(row => {{
      const cells = row.querySelectorAll('.line-card');
      let visibleInRow = false;
      cells.forEach(cell => {{
        const text = cell.textContent.toLowerCase();
        const match = text.includes(term);
        cell.parentElement.style.display = match ? '' : 'none';
        if (match) visibleInRow = true;
      }});
      row.style.display = visibleInRow ? '' : 'none';
    }});
  }});
</script>

</body>
</html>
"""

# === Build index rows ===
line_rows = ""
cols_per_row = 5

for i in range(0, len(line_ids), cols_per_row):
    row = line_ids[i:i + cols_per_row]
    row_html = '<div class="index-row">\n'
    for line_id in row:
        row_html += f'<div class="index-cell"><a class="line-card" href="lines/{line_id}.html">{line_id}</a></div>\n'
    row_html += '</div>\n'
    line_rows += row_html

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_template.format(line_rows=line_rows))

print("✅ Created: index.html")