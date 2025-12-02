#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

# Make the CSS work
python manage.py collectstatic --no-input

# Build the Database
python manage.py migrate
