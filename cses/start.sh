#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SCRIPT_DIR"

if [ "$#" -ne 1 ]; then
  printf 'Usage: %s <cses problem url>\n' "$0" >&2
  exit 1
fi

url="$1"
problem_id="${url##*/task/}"

if [ -z "$problem_id" ] || [ "$problem_id" = "$url" ] || [[ "$problem_id" == */* ]]; then
  printf 'Invalid CSES problem URL: %s\n' "$url" >&2
  exit 1
fi

title="$(curl -fsSL "$url" | sed -n 's|.*<title>CSES - \(.*\)</title>.*|\1|p' | head -n 1)"

if [ -z "$title" ]; then
  printf 'Failed to extract CSES title from: %s\n' "$url" >&2
  exit 1
fi

slug="$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g; s/-\{2,\}/-/g; s/^-//; s/-$//')"
dir_name="$problem_id-$slug"

mkdir -p "$dir_name"
echo "$url" > "$dir_name/link.txt"
cp "$REPO_ROOT/main.py" "$dir_name/main.py"
cp "$REPO_ROOT/main.hs" "$dir_name/main.hs"
cp "$REPO_ROOT/main.cpp" "$dir_name/main.cpp"
