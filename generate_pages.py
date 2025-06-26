import os
import sys
import json
from datetime import datetime

# Optional: specific line to generate
specific_line = sys.argv[1] if len(sys.argv) > 1 else None

# === CONFIGURATION ===
lines_folder = "lines"
images_folder = "Images"
filenames_path = "filenames.txt"
valid_ext = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

# === Load Line IDs ===
with open(filenames_path, "r", encoding="utf-8") as f:
    line_ids = [line.strip() for line in f if line.strip()]

# === HTML Page Template ===
page_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>RNAi Line {line}</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="apple-touch-icon" sizes="180x180" href="E:/RNAi Screening/favicon/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="E:/RNAi Screening/favicon/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="E:/RNAi Screening/favicon/favicon-16x16.png">
  <link rel="manifest" href="E:/RNAi Screening/favicon/site.webmanifest">
  <link rel="stylesheet" href="../style.css">
  <link href="https://cdn.jsdelivr.net/npm/glightbox/dist/css/glightbox.min.css" rel="stylesheet">
</head>
<body>

<button class="dark-toggle" onclick="toggleDarkMode()">🌙</button>
<button class="menu-toggle" onclick="toggleSidebar()">☰</button>

<div class="sidebar" id="sidebar">
  <h3>All Lines</h3>
  <button onclick="syncFromRender()" class="sync-button">🔁 Sync Uploads</button>
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

  <div class="upload-box">
    <form action="http://127.0.0.1:5000/" method="post" enctype="multipart/form-data" target="_blank">
      <input type="text" name="line_name" value="{line}" hidden>
      <input type="file" name="file" multiple required>
      <button type="submit">📤 Upload Images to {line}</button>
    </form>
  </div>

  <div class="image-gallery">
    {image_tags}
  </div>
</div>

<a href="../index.html" class="go-index">🏠 Index</a>

<script src="https://cdn.jsdelivr.net/npm/glightbox/dist/js/glightbox.min.js"></script>
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

  const lightbox = GLightbox({{
    selector: '.glightbox',
    touchNavigation: true,
    loop: true,
    zoomable: true,
    keyboardNavigation: true,
    openEffect: 'zoom',
    closeEffect: 'fade',
    slideEffect: 'slide',
    afterOpen: function() {{
      setTimeout(() => {{
        const btnSpan = document.querySelector('.gdesc #popup-delete-btn');
        if (btnSpan && !btnSpan.querySelector('button')) {{
          const line = btnSpan.getAttribute('data-line');
          const img = btnSpan.getAttribute('data-img');
          const btn = document.createElement('button');
          btn.textContent = '🗑️ Delete Image';
          btn.className = 'delete-image-btn';
          btn.onclick = function(e) {{
            e.preventDefault();
            if (!confirm('Are you sure you want to delete this image?')) return;
            fetch(`http://127.0.0.1:5000/delete_image`, {{
              method: 'POST',
              headers: {{'Content-Type': 'application/json'}},
              body: JSON.stringify({{ line: line, img: img }})
            }})
            .then(res => res.json())
            .then(data => {{
              if (data.success) {{
                alert('Image deleted! Reloading page...');
                window.location.reload();
              }} else {{
                alert('Failed to delete image: ' + data.error);
              }}
            }})
            .catch(() => alert('Failed to delete image (network error)'));
          }};
          btnSpan.appendChild(btn);
        }}
      }}, 100);
      const activeSlide = document.querySelector('.glightbox-active');
      if (activeSlide) {{
        activeSlide.scrollIntoView({{ block: 'center', behavior: 'smooth' }});
      }}
    }},
  }});
</script>

<script>
  function toggleDarkMode() {{
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
  }}

  window.addEventListener('DOMContentLoaded', () => {{
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {{
      document.body.classList.add('dark-mode');
    }}
  }});
</script>

<script>
function syncFromRender() {{
    fetch("sync_from_upload_server.bat")
        .then(() => alert("✅ Sync started!"))
        .catch(() => alert("❌ Sync failed. Check console."));
}}
</script>

<script>
document.addEventListener('click', function(e) {{
  if (e.target && e.target.classList.contains('delete-image-btn')) {{
    e.preventDefault();
    if (!confirm('Are you sure you want to delete this image?')) return;
    const line = e.target.getAttribute('data-line');
    const img = e.target.getAttribute('data-img');
    fetch(`http://127.0.0.1:5000/delete_image`, {{
      method: 'POST',
      headers: {{'Content-Type': 'application/json'}},
      body: JSON.stringify({{ line: line, img: img }})
    }})
    .then(res => res.json())
    .then(data => {{
      if (data.success) {{
        alert('Image deleted! Reloading page...');
        window.location.reload();
      }} else {{
        alert('Failed to delete image: ' + data.error);
      }}
    }})
    .catch(() => alert('Failed to delete image (network error)'));
  }}
}});
</script>

</body>
</html>
'''

# === Ensure folders exist ===
os.makedirs(lines_folder, exist_ok=True)

# === Generate Each Line Page ===
for line in line_ids:
    if specific_line and line != specific_line:
        continue

    image_folder = os.path.join(images_folder, line)
    desc_path = os.path.join(image_folder, "descriptions.json")
    if os.path.exists(desc_path):
        with open(desc_path, "r", encoding="utf-8") as f:
            descriptions = json.load(f)
    else:
        descriptions = {}

    valid_images = [
        img for img in os.listdir(image_folder)
        if os.path.splitext(img)[1].lower() in valid_ext
        and os.path.isfile(os.path.join(image_folder, img))
    ] if os.path.exists(image_folder) else []

    if valid_images:
        image_tags = "\n".join([
            f'''
            <div class="img-wrapper">
              <a href="../Images/{line}/{img}" class="glightbox"
                  data-gallery="gallery-{line}"
                  data-title="{descriptions.get(img, {}).get('caption', '') or os.path.splitext(img)[0]}"
                  data-description="{descriptions.get(img, {}).get('description', '')}<br><small><i>Uploaded: {datetime.fromtimestamp(os.path.getmtime(os.path.join(image_folder, img))).strftime('%Y-%m-%d %H:%M')}</i></small><span id='popup-delete-btn' data-line='{line}' data-img='{img}'></span>">
                <img src="../Images/{line}/{img}" alt="{img}" title="{descriptions.get(img, {}).get('caption', '') or os.path.splitext(img)[0]}">
              </a>
              <div class="image-caption">{descriptions.get(img, {}).get('caption', '') or os.path.splitext(img)[0]}</div>
            </div>
            ''' for img in valid_images
        ])
    else:
        image_tags = "<p style='text-align:center; color:#999;'>No images available for this line.</p>"

    sidebar_links = ""
    for other_id in line_ids:
        other_folder = os.path.join(images_folder, other_id)
        count = len([
            img for img in os.listdir(other_folder)
            if os.path.splitext(img)[1].lower() in valid_ext
            and os.path.isfile(os.path.join(other_folder, img))
        ]) if os.path.exists(other_folder) else 0

        count_span = f'<span class="img-count">{count}</span>' if count > 0 else ""
        active_class = "active-link" if other_id == line else ""
        active_id = 'id="activeLink"' if other_id == line else ""

        sidebar_links += (
            f'<a href="{other_id}.html" class="sidebar-link {active_class}" {active_id}>'
            f'<span class="line-name">{other_id}</span>{count_span}</a>\n'
        )

    html_content = page_template.format(
        line=line,
        sidebar_links=sidebar_links,
        image_tags=image_tags
    )

    output_path = os.path.join(lines_folder, f"{line}.html")
    with open(output_path, "w", encoding="utf-8", errors="ignore") as f:
        f.write(html_content)

    print(f"✅ Created: {output_path}")

# === Generate Index Page if no specific line ===
if not specific_line:
    index_template = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>RNAi Screening Index</title>
  <link rel="stylesheet" href="style.css">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="manifest" href="/site.webmanifest">
</head>
<body>
  <button class="dark-toggle" onclick="toggleDarkMode()">🌙</button>
  <h1 class="page-title">RNAi Line Navigator</h1>
  <p style="text-align:center;">
    <a href="http://127.0.0.1:5000/" target="_blank" class="go-index">📤 Upload Image</a>
  </p>

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

  function toggleDarkMode() {{
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('theme', document.body.classList.contains('dark-mode') ? 'dark' : 'light');
  }}

  window.addEventListener('DOMContentLoaded', () => {{
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {{
      document.body.classList.add('dark-mode');
    }}
  }});
</script>

</body>
</html>
'''

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