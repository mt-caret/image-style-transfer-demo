import hashlib
import os
import sys

from redis import Redis
from rq import Queue
q = Queue(connection=Redis())

sys.path.append('fast-style-transfer')
sys.path.append('fast-style-transfer/src') # A terrible hack
from evaluate import ffwd_to_img

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

CHECKPOINT_FILE = 'fast-style-transfer/models/udnie.ckpt'

TMP_DIR = '/tmp'

def convert_image(in_path, out_path):
    ffwd_to_img(in_path, out_path, CHECKPOINT_FILE)

def get_path(filename):
    return os.path.join(TMP_DIR, filename)

def exists(filename):
    return os.path.exists(get_path(filename))

def get_file(contents, extension):
    digest = hashlib.sha256(contents).hexdigest()

    out_filename = digest + '.' + extension
    out_path = os.path.join(TMP_DIR, out_filename)
    
    in_filename = '_' + out_filename
    in_path = os.path.join(TMP_DIR, in_filename)

    if not os.path.exists(out_path):
        with open(in_path, 'bw') as f:
            f.write(contents)
        q.enqueue(convert_image, in_path, out_path)

    return out_filename

