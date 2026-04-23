#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SCRIPT_DIR"

if [ "$#" -ne 1 ]; then
  printf 'Usage: %s <codewars kata url>\n' "$0" >&2
  exit 1
fi

url="$1"

if [[ ! "$url" =~ ^https?://(www\.)?codewars\.com/kata/([^/]+)/train/cpp/?$ ]]; then
  printf 'Invalid Codewars kata URL (expected .../kata/<slug>/train/cpp): %s\n' "$url" >&2
  exit 1
fi

title="$(curl -fsSL "$url" | sed -n 's#.*<title>\(.*\) | Codewars</title>.*#\1#p' | head -n 1)"
title="${title#Training on }"

if [ -z "$title" ]; then
  printf 'Failed to extract Codewars title from: %s\n' "$url" >&2
  exit 1
fi

mkdir -p "$title"
echo "$url" > "$title/link.txt"
cp "$REPO_ROOT/main.py" "$title/main.py"
cp "$REPO_ROOT/main.hs" "$title/main.hs"
cp "$REPO_ROOT/main.cpp" "$title/main.cpp"
