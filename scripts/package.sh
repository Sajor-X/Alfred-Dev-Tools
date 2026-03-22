#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

WORKFLOW_NAME="Alfred-Dev-Tools"
GITHUB_URL="https://github.com/Sajor-X/Alfred-Dev-Tools"

if [[ $# -gt 1 ]]; then
  echo "Usage: ./scripts/package.sh [version]" >&2
  exit 1
fi

if [[ $# -eq 1 ]]; then
  VERSION="$1"
  /usr/libexec/PlistBuddy -c "Set :version ${VERSION}" info.plist
else
  VERSION="$(/usr/libexec/PlistBuddy -c 'Print :version' info.plist)"
fi

PACKAGE_NAME="${WORKFLOW_NAME}-${VERSION}.alfredworkflow"

rm -f "${WORKFLOW_NAME}.alfredworkflow" "${PACKAGE_NAME}"

zip -r "${PACKAGE_NAME}" \
  info.plist README.md LICENSE icon.png \
  md5.py passwords.py start_timer.py timer_worker.py ts.py \
  b64.py jsonfmt.py urlencode.py urldecode.py sha.py uuidgen.py \
  textstat.py caseconv.py htmlcodec.py jwt.py \
  alfred_password_workflow docs scripts .gitignore \
  -x '*/__pycache__/*' '*.pyc' '.DS_Store'

plutil -lint info.plist

unzip -p "${PACKAGE_NAME}" info.plist | grep -nE \
  "<key>version</key>|<key>webaddress</key>|${VERSION}|${GITHUB_URL}"

ls -lh "${PACKAGE_NAME}"

echo "Packaged ${PACKAGE_NAME}"
