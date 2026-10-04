#!/bin/sh
set -eu
archive="qgis-jev-review-0.1.0.zip"
staging="$(mktemp -d)"
trap 'rm -rf "$staging"' EXIT
mkdir "$staging/qgis_jev_review"
cp __init__.py metadata.txt "$staging/qgis_jev_review/"
cp -R jev_qgis_review "$staging/qgis_jev_review/"
rm -f "$archive"
(cd "$staging" && zip -r "$OLDPWD/$archive" qgis_jev_review -x '*__pycache__*' '*.pyc')
echo "$archive"
