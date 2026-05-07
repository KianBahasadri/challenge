#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SCRIPT_DIR"

if [ "$#" -ne 1 ]; then
  printf 'Usage: %s <atcoder problem url>\n' "$0" >&2
  exit 1
fi

url="$1"

if [[ ! "$url" =~ ^https?://atcoder\.jp/contests/([^/]+)/tasks/([^/?#]+)/?$ ]]; then
  printf 'Invalid AtCoder problem URL (expected .../contests/<contest>/tasks/<task>): %s\n' "$url" >&2
  exit 1
fi

task_id="${BASH_REMATCH[2]}"
problem_id="$(printf '%s' "$task_id" | tr '[:upper:]_' '[:lower:]-')"

title="$(curl -fsSL "$url" | perl -0777 -ne '
  if (/<title>\s*(.*?)\s*-\s*AtCoder\s*<\/title>/is) {
    $title = $1;
    $title =~ s/^\s*[A-Z]\s*-\s*//;
    $title =~ s/\s+/ /g;
    $title =~ s/^\s+|\s+$//g;
    print $title;
  }
')"

if [ -z "$title" ]; then
  printf 'Failed to extract AtCoder title from: %s\n' "$url" >&2
  exit 1
fi

slug="$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g; s/-\{2,\}/-/g; s/^-//; s/-$//')"
dir_name="$problem_id-$slug"

mkdir -p "$dir_name"
echo "$url" > "$dir_name/link.txt"
cp "$REPO_ROOT/main.py" "$dir_name/main.py"
cp "$REPO_ROOT/main.hs" "$dir_name/main.hs"
cp "$REPO_ROOT/main.cpp" "$dir_name/main.cpp"
