#!/usr/bin/env python
from flask import Flask, request, send_file, jsonify
app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # maximum upload size

from convert import get_file, exists, get_path

ALLOWED_EXTENSIONS = set(['png'])

def extract_extension(filename):
    return filename.rsplit('.', 1)[1].lower()

def allowed_file(filename):
    return '.' in filename and extract_extension(filename) in ALLOWED_EXTENSIONS

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        abort(400)
    file = request.files['file']
    if file.filename == '':
        abort(400)
    if file and allowed_file(file.filename):
        out_path = get_file(file.read(), extract_extension(file.filename))
        return jsonify({ 'filename': out_path })
#        return send_file(out_path, mimetype='image/png');

@app.route('/query/<string:filename>', methods=['GET'])
def query(filename):
    return jsonify({ 'done': exists(filename) })

@app.route('/result/<string:filename>', methods=['GET'])
def result(filename):
    return send_file(get_path(filename))

@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
