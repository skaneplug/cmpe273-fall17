import subprocess
from flask import Flask, redirect, url_for, request, jsonify
import sqlite3
import os
import socket

#File Upload
UPLOAD_FOLDER = 'uploads_py'
ALLOWED_EXTENSIONS = set(['py'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

SCID = 0
#DB Connection

def get_scriptId():
    global SCID
    SCID += 1
    return SCID


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def run_script(id):
    """
    Return a string that is the output from subprocess
    """
    path = UPLOAD_FOLDER + "/" + id + '.py'
    p = subprocess.Popen(['python3', path], stdout=subprocess.PIPE)
    out, err = p.communicate()
    return out

@app.route('/')
def index():
    return 'welcome'

@app.route('/api/v1/scripts', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['data']
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            script_id = get_scriptId()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(script_id)+".py"))
            return jsonify({"script-id": script_id})

@app.route('/api/v1/scripts/<id>')
def render2(id):
    get_scriptId()
    return run_script(id)

@app.route('/hello')
def hello():
    html = "<h3>Hello? {name}!</h3>" \
           "<b>Hostname:</b> {hostname}<br/>" \
           "<b>Visits:</b> {visits}"
    return html.format(name=os.getenv("NAME", "world"), hostname=socket.gethostname())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
