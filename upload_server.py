# upload_server.py
import os
from flask import Flask, request, render_template_string, redirect, url_for

app = Flask(__name__)

UPLOAD_ROOT = os.path.join(os.getcwd(), 'Images')  # must match your structure
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

# --- HTML Upload Page Template ---
upload_form = """
<!DOCTYPE html>
<html>
<head>
  <title>Upload RNAi Image</title>
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>
  <h1 class="page-title">Upload Image to RNAi Line</h1>
  <form action="/" method="POST" enctype="multipart/form-data">
    <label>Select RNAi Line:</label><br>
    <input type="text" name="line_id" required placeholder="e.g. 25799"><br><br>

    <label>Select Image:</label><br>
    <input type="file" name="image" accept="image/*" required><br><br>

    <button type="submit">Upload</button>
  </form>

  {% if msg %}
  <p style="color: green;">{{ msg }}</p>
  {% endif %}
</body>
</html>
"""

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def upload_image():
    msg = ""
    if request.method == "POST":
        line_id = request.form.get("line_id")
        file = request.files.get("image")
        if file and allowed_file(file.filename):
            save_path = os.path.join(UPLOAD_ROOT, line_id)
            os.makedirs(save_path, exist_ok=True)
            file.save(os.path.join(save_path, file.filename))
            msg = f"✅ Uploaded successfully to {line_id}/"
        else:
            msg = "❌ Invalid file type."

    return render_template_string(upload_form, msg=msg)

if __name__ == "__main__":
    app.run(debug=True)
