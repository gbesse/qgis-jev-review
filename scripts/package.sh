#!/bin/sh
set -eu
archive="qgis-jev-review-0.1.0.zip"
zip -r "$archive" __init__.py metadata.txt jev_qgis_review -x '*__pycache__*' '*.pyc'
echo "$archive"
