#!/usr/bin/env bash

set -euo pipefail

if [ "$#" -ne 1 ]; then
  printf 'Usage: %s <dmoj problem url>\n' "$0" >&2
  exit 1
fi

url="$1"
problem_id="${url##*/problem/}"

if [ -z "$problem_id" ] || [ "$problem_id" = "$url" ] || [[ "$problem_id" == */* ]]; then
  printf 'Invalid DMOJ problem URL: %s\n' "$url" >&2
  exit 1
fi

mkdir -p "$problem_id"
echo "$url" > "$problem_id/link.txt"
cp main.py "$problem_id/main.py"
cp main.hs "$problem_id/main.hs"
