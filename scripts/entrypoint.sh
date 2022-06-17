#!/bin/sh

set -ex

python -u ~/scripts/setup_app.py
exec python -u "$APP_NAME" "$@"
