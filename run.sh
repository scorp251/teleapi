#!/usr/bin/env bash

gunicorn -b 0.0.0.0:5000 --reload app:app
