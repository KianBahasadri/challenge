#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SCRIPT_DIR"

if [ "$#" -ne 1 ]; then
  printf 'Usage: %s <yosupo problem url>\n' "$0" >&2
  exit 1
fi

url="$1"

if [[ ! "$url" =~ ^https?://judge\.yosupo\.jp/problem/([^/?#]+)/?$ ]]; then
  printf 'Invalid Yosupo problem URL (expected .../problem/<problem_id>): %s\n' "$url" >&2
  exit 1
fi

problem_id="$(printf '%s' "${BASH_REMATCH[1]}" | tr '[:upper:]_' '[:lower:]-')"

mkdir -p "$problem_id"
echo "$url" > "$problem_id/link.txt"
cp "$REPO_ROOT/main.py" "$problem_id/main.py"
cp "$REPO_ROOT/main.hs" "$problem_id/main.hs"
cp "$REPO_ROOT/main.cpp" "$problem_id/main.cpp"
