#!/usr/bin/env bash

cd /opt/teleapi

./.venv/bin/activate

gunicorn -b 127.0.0.1:5000 --reload app:app
