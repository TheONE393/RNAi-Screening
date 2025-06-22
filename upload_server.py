from flask import Flask, request, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

UPLOAD_FOLDER = 'Images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = '''
<!doctype html>
<title>RNAi Image Uploader</title>
<h2>Upload Image for RNAi Line</h2>
<form method=post enctype=multipart/form-data>
  Line Name: <input type=text name=line_name required><br><br>
  <input type=file name=file required>
  <input type=submit value=Upload>
</form>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        line_name = request.form['line_name'].strip().replace(" ", "_")
        files = request.files.getlist('file')  # Handle multiple files
        save_path = os.path.join(UPLOAD_FOLDER, line_name)
        os.makedirs(save_path, exist_ok=True)

        uploaded = 0
        for file in files:
            if file:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{timestamp}_{file.filename}"
                file.save(os.path.join(save_path, filename))
                uploaded += 1

        return f"✅ Uploaded <b>{uploaded}</b> file(s) to <b>{line_name}</b>!"
    
    return render_template_string(HTML_TEMPLATE)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Accepts external connections on LAN if needed
