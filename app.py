import hashlib
import os
from flask import Flask, request, send_file
app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # maximum upload size

ALLOWED_EXTENSIONS = set(['png'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/convert', methods=['POST'])
def convert():
	if 'file' not in request.files:
		abort(400)
	file = request.files['file']
	print("filename: " + file.filename)
	if file.filename == '':
		abort(400)
	if file and allowed_file(file.filename):
		contents = file.read()
		filename = hashlib.sha256(contents).hexdigest() + '.png'
		path = os.path.join('/tmp', filename)
		with open(path, 'w') as f:
			f.write(contents)
		print(path)
		return send_file(path, mimetype='image/png');

@app.route('/')
def root():
	return app.send_static_file('index.html')
