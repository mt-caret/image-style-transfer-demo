import hashlib
import sys
import os

from flask import Flask, request, send_file
app = Flask(__name__, static_url_path='')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # maximum upload size

sys.path.append('fast-style-transfer')
sys.path.append('fast-style-transfer/src') # A terrible hack
from evaluate import ffwd_to_img

ALLOWED_EXTENSIONS = set(['png'])

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

CHECKPOINT_FILE = 'fast-style-transfer/models/udnie.ckpt'

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        abort(400)
    file = request.files['file']
    if file.filename == '':
        abort(400)
    if file and allowed_file(file.filename):
        contents = file.read()
        digest = hashlib.sha256(contents).hexdigest()
        in_filename = digest + '.png'
        in_path = os.path.join('/tmp', in_filename)
        out_filename = digest + '_conv.png'
        out_path = os.path.join('/tmp', out_filename)

        if not os.path.exists(out_path):
            with open(in_path, 'bw') as f:
                f.write(contents)
            ffwd_to_img(in_path, out_path, CHECKPOINT_FILE)

        return send_file(out_path, mimetype='image/png');

@app.route('/')
def root():
    return app.send_static_file('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)
