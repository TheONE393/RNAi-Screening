from flask import Flask, request, jsonify
import os

app = Flask(__name__)
UPLOAD_FOLDER = "Images"

@app.route("/upload", methods=["POST"])
def upload():
    line_id = request.form.get("line_id")
    files = request.files.getlist("images")

    if not line_id or not files:
        return "Missing line_id or files", 400

    save_dir = os.path.join(UPLOAD_FOLDER, line_id)
    os.makedirs(save_dir, exist_ok=True)

    for file in files:
        filepath = os.path.join(save_dir, file.filename)
        file.save(filepath)

    return f"✅ Uploaded {len(files)} image(s) to line {line_id}"

if __name__ == "__main__":
    app.run(debug=True)
