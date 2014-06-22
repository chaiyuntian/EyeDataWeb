import os
from flask import Flask, request, redirect, url_for, jsonify, render_template
from werkzeug.utils import secure_filename
from eyedata.packData import *
import json

UPLOAD_FOLDER = 'static' + os.sep + 'Uploads'
ALLOWED_EXTENSIONS = set(['xlsx', 'xls'])
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    return render_template('AjaxTest.html')


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file1 = request.files['file']
        if file1 and allowed_file(file1.filename):
            filename = secure_filename(file1.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file1.save(filepath)
            result = jsonify(calc_return(filepath))
            return result
            #redirect(url_for('uploaded_file',filename=filename))

    '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form> '''


from flask import send_from_directory


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


app.run("192.168.1.104", 5555, debug=True)