# upload_server.py

from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "Images")

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload/<line_id>', methods=['POST'])
def upload_images(line_id):
    if 'images' not in request.files:
        return jsonify({"error": "No files provided"}), 400

    files = request.files.getlist('images')
    line_folder = os.path.join(app.config['UPLOAD_FOLDER'], line_id)

    if not os.path.exists(line_folder):
        os.makedirs(line_folder)

    saved_files = []

    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(line_folder, filename))
            saved_files.append(filename)

    if saved_files:
        print(f"✅ Uploaded to line {line_id}: {', '.join(saved_files)}")
        return jsonify({"success": f"Files uploaded to line {line_id}", "files": saved_files}), 200
    else:
        return jsonify({"error": "No valid images uploaded"}), 400

if __name__ == '__main__':
    app.run(debug=True)
