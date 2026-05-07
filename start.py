#!/usr/bin/env python3

from __future__ import annotations

import html
import json
import re
import shutil
import sys
import urllib.request
from pathlib import Path
from urllib.error import URLError


class StartError(Exception):
    pass


def fetch_text(url: str) -> str:
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request) as response:
            return response.read().decode("utf-8", errors="replace")
    except URLError as exc:
        raise StartError(f"Failed to fetch {url}: {exc}") from exc


def slug_hyphen(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return slug.strip("-")


def slug_codewars(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()
    return re.sub(r" +", "_", cleaned)


def create_problem(platform_dir: Path, repo_root: Path, dirname: str, url: str) -> None:
    if not dirname:
        raise StartError("Generated an empty problem directory name")

    problem_dir = platform_dir / dirname
    problem_dir.mkdir(parents=True, exist_ok=True)
    (problem_dir / "link.txt").write_text(f"{url}\n")

    for template in ("main.py", "main.hs", "main.cpp"):
        shutil.copyfile(repo_root / template, problem_dir / template)


def parse_atcoder(url: str) -> str:
    match = re.fullmatch(r"https?://atcoder\.jp/contests/([^/]+)/tasks/([^/?#]+)/?", url)
    if not match:
        raise StartError(
            f"Invalid AtCoder problem URL (expected .../contests/<contest>/tasks/<task>): {url}"
        )

    task_id = match.group(2)
    problem_id = task_id.lower().replace("_", "-")
    page = fetch_text(url)
    title_match = re.search(r"<title>\s*(.*?)\s*-\s*AtCoder\s*</title>", page, re.I | re.S)
    if not title_match:
        raise StartError(f"Failed to extract AtCoder title from: {url}")

    title = re.sub(r"^\s*[A-Z]\s*-\s*", "", html.unescape(title_match.group(1)))
    title = re.sub(r"\s+", " ", title).strip()
    return f"{problem_id}-{slug_hyphen(title)}"


def parse_codechef(url: str) -> str:
    match = re.fullmatch(
        r"https?://(?:www\.)?codechef\.com/practice/course/[^/]+/[^/]+/problems/([^/?#]+)/?",
        url,
    )
    if not match:
        raise StartError(
            "Invalid CodeChef problem URL "
            f"(expected .../practice/course/<course>/<difficulty>/problems/<code>): {url}"
        )

    return match.group(1).lower()


def parse_codeforces(url: str) -> str:
    match = re.fullmatch(r"https?://codeforces\.com/contest/([0-9]+)/problem/([^/?#]+)/?", url)
    if not match:
        match = re.fullmatch(
            r"https?://codeforces\.com/problemset/problem/([0-9]+)/([^/?#]+)/?", url
        )
    if not match:
        raise StartError(
            "Invalid Codeforces problem URL "
            f"(expected .../contest/<id>/problem/<index> or .../problemset/problem/<id>/<index>): {url}"
        )

    contest_id = int(match.group(1))
    problem_index = match.group(2).lower()
    data = json.loads(fetch_text("https://codeforces.com/api/problemset.problems"))

    title = ""
    for problem in data["result"]["problems"]:
        if (
            problem.get("contestId") == contest_id
            and problem.get("index", "").upper() == problem_index.upper()
        ):
            title = problem["name"]
            break

    if not title:
        raise StartError(f"Failed to extract Codeforces title from: {url}")

    return f"{contest_id}-{problem_index}-{slug_hyphen(title)}"


def parse_codewars(url: str) -> str:
    match = re.fullmatch(r"https?://(?:www\.)?codewars\.com/kata/([^/]+)/train/cpp/?", url)
    if not match:
        raise StartError(f"Invalid Codewars kata URL (expected .../kata/<slug>/train/cpp): {url}")

    page = fetch_text(url)
    title_match = re.search(r"<title>(.*?) \| Codewars</title>", page, re.I | re.S)
    if not title_match:
        raise StartError(f"Failed to extract Codewars title from: {url}")

    title = title_match.group(1).removeprefix("Training on ")
    dirname = slug_codewars(title)
    if not dirname:
        raise StartError(f"Failed to generate a valid directory name from title: {title}")
    return dirname


def parse_cses(url: str) -> str:
    marker = "/task/"
    if marker not in url:
        raise StartError(f"Invalid CSES problem URL: {url}")

    problem_id = url.rsplit(marker, 1)[1]
    if not problem_id or "/" in problem_id.strip("/"):
        raise StartError(f"Invalid CSES problem URL: {url}")
    problem_id = problem_id.rstrip("/")

    page = fetch_text(url)
    title_match = re.search(r"<title>CSES - (.*?)</title>", page, re.I | re.S)
    if not title_match:
        raise StartError(f"Failed to extract CSES title from: {url}")

    title = html.unescape(title_match.group(1))
    return f"{problem_id}-{slug_hyphen(title)}"


def parse_dmoj(url: str) -> str:
    marker = "/problem/"
    if marker not in url:
        raise StartError(f"Invalid DMOJ problem URL: {url}")

    problem_id = url.rsplit(marker, 1)[1]
    if not problem_id or "/" in problem_id.strip("/"):
        raise StartError(f"Invalid DMOJ problem URL: {url}")
    return problem_id.rstrip("/")


def parse_hackerrank(url: str) -> str:
    match = re.search(r"https?://(?:www\.)?hackerrank\.com/challenges/([^/]+)/problem", url)
    if not match:
        raise StartError(
            f"Invalid HackerRank problem URL (expected .../challenges/<name>/problem): {url}"
        )

    return match.group(1)


def parse_project_euler(url: str) -> tuple[str, str]:
    match = re.fullmatch(r"https?://(?:www\.)?projecteuler\.net/problem=([0-9]+)/?", url)
    if not match:
        raise StartError(
            f"Invalid Project Euler problem URL (expected https://projecteuler.net/problem=<number>): {url}"
        )

    problem_id = match.group(1)
    description = fetch_text(f"https://projecteuler.net/minimal={problem_id}")
    return problem_id, description


def parse_usaco(url: str) -> str:
    match = re.match(r"https?://(?:www\.)?usaco\.org/index\.php\?page=viewproblem2&cpid=([0-9]+)", url)
    if not match:
        raise StartError(
            f"Invalid USACO problem URL (expected ...index.php?page=viewproblem2&cpid=<id>): {url}"
        )

    problem_id = match.group(1)
    page = fetch_text(url)
    title_match = re.search(r"Problem\s+\d+\.\s*(.*?)\s*(?:<|\n)", page, re.I | re.S)
    if not title_match:
        raise StartError(f"Failed to extract USACO title from: {url}")

    title = re.sub(r"<[^>]+>", "", title_match.group(1))
    title = re.sub(r"\s+", " ", html.unescape(title)).strip()
    return f"{problem_id}-{slug_hyphen(title)}"


def parse_yosupo(url: str) -> str:
    match = re.fullmatch(r"https?://judge\.yosupo\.jp/problem/([^/?#]+)/?", url)
    if not match:
        raise StartError(f"Invalid Yosupo problem URL (expected .../problem/<problem_id>): {url}")

    return match.group(1).lower().replace("_", "-")


PARSERS = {
    "atcoder": parse_atcoder,
    "codechef": parse_codechef,
    "codeforces": parse_codeforces,
    "codewars": parse_codewars,
    "cses": parse_cses,
    "dmoj": parse_dmoj,
    "hackerrank": parse_hackerrank,
    "usaco": parse_usaco,
    "yosupo": parse_yosupo,
}


def main(argv: list[str]) -> int:
    invoked = Path(argv[0])
    platform_dir = (Path.cwd() / invoked.parent).resolve() if not invoked.is_absolute() else invoked.parent.resolve()
    repo_root = platform_dir.parent
    platform = platform_dir.name

    if len(argv) != 2:
        label = platform.replace("_", " ").title()
        print(f"Usage: {argv[0]} <{label} problem url>", file=sys.stderr)
        return 1

    url = argv[1]
    try:
        if platform == "project_euler":
            dirname, description = parse_project_euler(url)
            create_problem(platform_dir, repo_root, dirname, url)
            (platform_dir / dirname / "description.md").write_text(description)
        else:
            parser = PARSERS.get(platform)
            if parser is None:
                raise StartError(f"Unsupported platform directory: {platform}")
            dirname = parser(url)
            create_problem(platform_dir, repo_root, dirname, url)
    except StartError as exc:
        print(exc, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
