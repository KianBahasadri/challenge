#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$SCRIPT_DIR"

usage() {
  printf 'Usage: %s [--list] <usaco.guide module url>\n' "$0" >&2
}

list_only=0
if [ "${1:-}" = "--list" ]; then
  list_only=1
  shift
fi

if [ "$#" -ne 1 ]; then
  usage
  exit 1
fi

module_url="$1"
if [[ ! "$module_url" =~ ^https?://usaco\.guide/([^/?#]+)/([^/?#]+) ]]; then
  printf 'Invalid USACO Guide module URL: %s\n' "$module_url" >&2
  exit 1
fi

division="${BASH_REMATCH[1]}"
module="${BASH_REMATCH[2]}"

slugify() {
  printf '%s' "$1" |
    tr '[:upper:]' '[:lower:]' |
    sed 's/[^a-z0-9]/-/g; s/-\{2,\}/-/g; s/^-//; s/-$//'
}

extract_problems() {
  perl -0777 -ne '
    sub clean {
      my ($s) = @_;
      $s =~ s/<script\b.*?<\/script>//gis;
      $s =~ s/<style\b.*?<\/style>//gis;
      $s =~ s/<[^>]+>//g;
      $s =~ s/<!--.*?-->//gs;
      $s =~ s/&amp;/\&/g;
      $s =~ s/&quot;/"/g;
      $s =~ s/&#x27;/'"'"'/g;
      $s =~ s/&lt;/</g;
      $s =~ s/&gt;/>/g;
      $s =~ s/\s+/ /g;
      $s =~ s/^\s+|\s+$//g;
      return $s;
    }

    while (/id="problem-([^"]+)"(.*?)(?=id="problem-|<h2\b|$)/gs) {
      my ($id, $chunk) = ($1, $2);
      next unless $chunk =~ /<a\b[^>]*href="([^"]+)"[^>]*>(.*?)<\/a>/s;
      my ($url, $anchor) = (clean($1), $2);

      my $title = "";
      if ($anchor =~ /text-lg font-medium[^>]*>([^<]+)/s) {
        $title = clean($1);
      } else {
        $title = clean($anchor);
      }
      next if $title eq "";

      my $source = $id;
      $source =~ s/-.*//;
      my $difficulty = "";
      if ($chunk =~ /rounded-full[^>]*>([^<]+)<\/span>/s) {
        $difficulty = clean($1);
      } elsif ($chunk =~ /mt-1 text-sm[^>]*>(.*?)<\/div>/s) {
        my $meta = clean($1);
        $difficulty = $meta;
        $difficulty =~ s/^.* - //;
      }

      print join("\t", $id, $source, $difficulty, $url, $title), "\n";
    }
  '
}

html="$(curl -fsSL "$module_url")"
problems="$(printf '%s' "$html" | extract_problems)"

if [ -z "$problems" ]; then
  printf 'No problem cards found in: %s\n' "$module_url" >&2
  exit 1
fi

printf 'Problems in %s/%s:\n' "$division" "$module"
awk -F '\t' '{ printf "%2d. [%s] %s", NR, $2, $5; if ($3 != "") printf " (%s)", $3; printf "\n    %s\n", $4 }' <<< "$problems"

if [ "$list_only" -eq 1 ]; then
  exit 0
fi

mkdir -p "$division/$module"

while IFS= read -r row; do
  IFS=$'\t' read -r problem_id source difficulty url title <<< "$row"
  dir_slug="$(slugify "$problem_id-$title")"
  problem_dir="$division/$module/$dir_slug"

  if [ -d "$problem_dir" ]; then
    status="Exists"
  else
    mkdir -p "$problem_dir"
    status="Created"
  fi

  [ -e "$problem_dir/link.txt" ] || printf '%s\n' "$url" > "$problem_dir/link.txt"

  [ -e "$problem_dir/main.py" ] || cp "$REPO_ROOT/main.py" "$problem_dir/main.py"
  [ -e "$problem_dir/main.hs" ] || cp "$REPO_ROOT/main.hs" "$problem_dir/main.hs"
  [ -e "$problem_dir/main.cpp" ] || cp "$REPO_ROOT/main.cpp" "$problem_dir/main.cpp"

  printf '%s %s\n' "$status" "$problem_dir"
done <<< "$problems"
