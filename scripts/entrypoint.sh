#!/bin/sh

set -ex

python -u ~/scripts/setup_app.py
python -u "$APP_NAME" "$@"
