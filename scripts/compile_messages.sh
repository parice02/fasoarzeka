#!/usr/bin/env bash
# Compile .po files into .mo files
set -euo pipefail

LOCALES_DIR="locales"

if [ ! -d "$LOCALES_DIR" ]; then
  echo "No locales directory found. Run extract_messages.sh first."
  exit 1
fi

for po in $(find "$LOCALES_DIR" -name '*.po'); do
  mo_dir=$(dirname "$po")
  mo_dir=${mo_dir%/LC_MESSAGES}
  mo_dir="$mo_dir/LC_MESSAGES"
  mkdir -p "$mo_dir"
  mo_file="$mo_dir/$(basename "$po" .po).mo"
  echo "Compiling $po -> $mo_file"
  msgfmt "$po" -o "$mo_file"
done

echo "Compilation terminée."
