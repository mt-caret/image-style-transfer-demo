#!/usr/bin/env /bin/bash
set -e
FLASK_DEBUG=1 FLASK_APP=app.py flask run --host=0.0.0.0

