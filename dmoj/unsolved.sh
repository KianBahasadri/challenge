#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

for d in "$SCRIPT_DIR"/*; do
  [ -d "$d" ] || continue
  if [ ! -f "$d/submission.txt" ]; then
    printf '%s\n' "${d##*/}"
  fi
done
