#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SCRIPT_DIR"

if [ "$#" -ne 1 ]; then
  printf 'Usage: %s <project euler problem url>\n' "$0" >&2
  exit 1
fi

url="$1"

if [[ ! "$url" =~ ^https?://(www\.)?projecteuler\.net/problem=([0-9]+)/?$ ]]; then
  printf 'Invalid Project Euler problem URL (expected https://projecteuler.net/problem=<number>): %s\n' "$url" >&2
  exit 1
fi

problem_id="${BASH_REMATCH[2]}"
problem_dir="$problem_id"
minimal_url="https://projecteuler.net/minimal=$problem_id"

mkdir -p "$problem_dir"
echo "$url" > "$problem_dir/link.txt"
cp "$REPO_ROOT/main.py" "$problem_dir/main.py"
cp "$REPO_ROOT/main.hs" "$problem_dir/main.hs"
curl -fsSL "$minimal_url" -o "$problem_dir/description.md"
