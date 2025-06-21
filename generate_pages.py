import os

# === CONFIGURATION ===
lines_folder = "lines"
images_folder = "images"
filenames_path = "filenames.txt"

# === Load RNAi Line IDs ===
with open(filenames_path, "r", encoding="utf-8") as f:
    line_ids = [line.strip() for line in f if line.strip()]

# === Ensure all image folders exist and have a .gitkeep if empty ===
for line in line_ids:
    folder_path = os.path.join(images_folder, line)
    os.makedirs(folder_path, exist_ok=True)
    is_empty = not any(fname for fname in os.listdir(folder_path) if not fname.startswith("."))
    if is_empty:
        gitkeep_path = os.path.join(folder_path, ".gitkeep")
        with open(gitkeep_path, "w") as f:
            f.write("")
        print(f"📝 Added .gitkeep to empty folder: {folder_path}")

# === HTML Template for Each Line ===
page_template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>RNAi Line {line}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="../style.css">
  <link href="https://cdn.jsdelivr.net/npm/lightbox2@2/dist/css/lightbox.min.css" rel="stylesheet">
</head>
<body>

<button class="menu-toggle" onclick="toggleSidebar()">☰</button>

<div class="sidebar" id="sidebar">
  <h3>All Lines</h3>
  <div class="search-box">
    <input type="text" id="sidebarSearch" placeholder="Search...">
  </div>
  <div class="sidebar-grid" id="sidebarLinks">
    {sidebar_links}
  </div>
</div>

<div class="content">
  <h1 class="page-title">RNAi Line {line}</h1>
  <p style="text-align:center; color:#666;">Notes and images for line {line}.</p>
  <div class="image-gallery">
    {image_tags}
  </div>
</div>

<a href="../index.html" class="go-index">🏠 Index</a>

<script src="https://cdn.jsdelivr.net/npm/lightbox2@2/dist/js/lightbox-plus-jquery.min.js"></script>
<script>
  function toggleSidebar() {{
    document.getElementById("sidebar").classList.toggle("open");
  }}

  window.onload = function() {{
    const active = document.getElementById("activeLink");
    if (active) {{
      active.scrollIntoView({{ block: "center", behavior: "smooth" }});
    }}
  }};

  const sidebarInput = document.getElementById('sidebarSearch');
  const sidebarLinks = document.getElementById('sidebarLinks');
  sidebarInput.addEventListener('input', () => {{
    const term = sidebarInput.value.toLowerCase();
    const links = sidebarLinks.querySelectorAll('a');
    links.forEach(link => {{
      link.style.display = link.textContent.toLowerCase().includes(term) ? '' : 'none';
    }});
  }});
</script>

</body>
</html>
"""

valid_ext = ['.jpg', '.jpeg', '.png', '.gif', '.webp']
os.makedirs(lines_folder, exist_ok=True)

# === Generate HTML for Each Line ===
for line in line_ids:
    image_folder = os.path.join(images_folder, line)
    images = sorted([img for img in os.listdir(image_folder) if os.path.splitext(img)[1].lower() in valid_ext]) if os.path.exists(image_folder) else []

    image_tags = ""
    for img in images:
        image_path = f"../images/{line}/{img}"
        image_tags += f'''
        <div class="image-block">
            <a href="{image_path}" data-lightbox="line-{line}" data-title="{img}">
                <img src="{image_path}" alt="{img}">
            </a>
            <div class="image-caption">{img}</div>
        </div>
        '''

    sidebar_links = ""
    for other_id in line_ids:
        other_folder = os.path.join(images_folder, other_id)
        other_images = [img for img in os.listdir(other_folder) if os.path.splitext(img)[1].lower() in valid_ext] if os.path.exists(other_folder) else []
        img_count = len(other_images)
        count_span = f'<span class="img-count">{img_count}</span>' if img_count > 0 else ""
        active_class = "active-link" if other_id == line else ""
        active_id = 'id="activeLink"' if other_id == line else ""

        sidebar_links += (
            f'<a href="{other_id}.html" class="sidebar-link {active_class}" {active_id}>'
            f'<span class="line-name">{other_id}</span>{count_span}</a>\n'
        )

    html_content = page_template.format(line=line, sidebar_links=sidebar_links, image_tags=image_tags)
    with open(os.path.join(lines_folder, f"{line}.html"), "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Created: lines/{line}.html")

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

line_rows = ""
cols_per_row = 5
for i in range(0, len(line_ids), cols_per_row):
    row = line_ids[i:i + cols_per_row]
    line_row_html = '<div class="index-row">\n'
    for line_id in row:
        line_row_html += f'<div class="index-cell"><a class="line-card" href="lines/{line_id}.html">{line_id}</a></div>\n'
    line_row_html += '</div>\n'
    line_rows += line_row_html

with open("index.html", "w", encoding="utf-8") as f:
    f.write(index_template.format(line_rows=line_rows))

print("✅ Created: index.html")
