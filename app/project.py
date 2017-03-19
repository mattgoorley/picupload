import os
from app import app
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = os.path.join(app.root_path, 'image')
ALLOWED_EXTENSIONS = set(['pdf','png','jpg','jpeg','gif'])


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'picture' not in request.files:
            flash('No file')
            return redirect(request.url)

        file = request.files['picture']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))

    return render_template('index.html')

@app.route('/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
