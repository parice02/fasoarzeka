#!/usr/bin/env bash
# Extract translatable strings into a POT template
set -euo pipefail

OUT_DIR="locales"
POT_FILE="$OUT_DIR/arzeka.pot"

mkdir -p "$OUT_DIR"

echo "Extracting messages to $POT_FILE"
# Use xgettext to extract strings marked with _()
# You may need to install gettext-tools (xgettext/msgfmt) on your system.
xgettext -k_ -o "$POT_FILE" $(find . -name '*.py') || true

echo "Extraction finished. Edit PO files in locales/<lang>/LC_MESSAGES/"
