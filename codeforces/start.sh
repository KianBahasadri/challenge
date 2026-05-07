#!/usr/bin/env bash

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SCRIPT_DIR"

if [ "$#" -ne 1 ]; then
  printf 'Usage: %s <codeforces problem url>\n' "$0" >&2
  exit 1
fi

url="$1"

if [[ "$url" =~ ^https?://codeforces\.com/contest/([0-9]+)/problem/([^/?#]+)/?$ ]]; then
  contest_id="${BASH_REMATCH[1]}"
  problem_index="${BASH_REMATCH[2]}"
elif [[ "$url" =~ ^https?://codeforces\.com/problemset/problem/([0-9]+)/([^/?#]+)/?$ ]]; then
  contest_id="${BASH_REMATCH[1]}"
  problem_index="${BASH_REMATCH[2]}"
else
  printf 'Invalid Codeforces problem URL (expected .../contest/<id>/problem/<index> or .../problemset/problem/<id>/<index>): %s\n' "$url" >&2
  exit 1
fi

problem_index="$(printf '%s' "$problem_index" | tr '[:upper:]' '[:lower:]')"

title="$(curl -fsSL 'https://codeforces.com/api/problemset.problems' | python3 -c '
import json
import sys

contest_id = int(sys.argv[1])
problem_index = sys.argv[2].upper()
data = json.load(sys.stdin)

for problem in data["result"]["problems"]:
    if problem.get("contestId") == contest_id and problem.get("index", "").upper() == problem_index:
        print(problem["name"])
        break
' "$contest_id" "$problem_index")"

if [ -z "$title" ]; then
  printf 'Failed to extract Codeforces title from: %s\n' "$url" >&2
  exit 1
fi

slug="$(printf '%s' "$title" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g; s/-\{2,\}/-/g; s/^-//; s/-$//')"
dir_name="$contest_id-$problem_index-$slug"

mkdir -p "$dir_name"
echo "$url" > "$dir_name/link.txt"
cp "$REPO_ROOT/main.py" "$dir_name/main.py"
cp "$REPO_ROOT/main.hs" "$dir_name/main.hs"
cp "$REPO_ROOT/main.cpp" "$dir_name/main.cpp"
