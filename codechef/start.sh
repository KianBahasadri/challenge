#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SCRIPT_DIR"

if [ "$#" -ne 1 ]; then
  printf 'Usage: %s <codechef problem url>\n' "$0" >&2
  exit 1
fi

url="$1"

if [[ ! "$url" =~ ^https?://(www\.)?codechef\.com/practice/course/[^/]+/[^/]+/problems/([^/?#]+)/?$ ]]; then
  printf 'Invalid CodeChef problem URL (expected .../practice/course/<course>/<difficulty>/problems/<code>): %s\n' "$url" >&2
  exit 1
fi

problem_id="$(printf '%s' "${BASH_REMATCH[2]}" | tr '[:upper:]' '[:lower:]')"

mkdir -p "$problem_id"
echo "$url" > "$problem_id/link.txt"
cp "$REPO_ROOT/main.py" "$problem_id/main.py"
cp "$REPO_ROOT/main.hs" "$problem_id/main.hs"
cp "$REPO_ROOT/main.cpp" "$problem_id/main.cpp"
