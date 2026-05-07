#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

OPEN=0
for arg in "$@"; do
  [ "$arg" = "--open" ] && OPEN=1
done

for d in "$SCRIPT_DIR"/*; do
  [ -d "$d" ] || continue
  if [ ! -f "$d/submission.txt" ] && [ ! -f "$d/completed" ]; then
    printf '%s\n' "${d##*/}"
    if [ "$OPEN" -eq 1 ] && [ -f "$d/link.txt" ]; then
      firefox "$(<"$d/link.txt")"
    fi
  fi
done
