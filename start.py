#!/usr/bin/env python3

from __future__ import annotations

import html
import json
import re
import shutil
import subprocess
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
        try:
            result = subprocess.run(
                ["curl", "-L", "-s", "--fail", "--max-time", "15", url],
                check=True,
                capture_output=True,
                text=True,
            )
            return result.stdout
        except (OSError, subprocess.CalledProcessError) as curl_exc:
            raise StartError(f"Failed to fetch {url}: {exc}; curl fallback failed: {curl_exc}") from exc


def slug_hyphen(text: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower())
    return slug.strip("-")


def slug_codewars(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()
    return re.sub(r" +", "_", cleaned)


LANGUAGE_TEMPLATES = {
    "--cpp": "main.cpp",
    "--py": "main.py",
    "--hs": "main.hs",
}


def create_problem(platform_dir: Path, repo_root: Path, dirname: str, url: str, template: str) -> None:
    if not dirname:
        raise StartError("Generated an empty problem directory name")

    problem_dir = platform_dir / dirname
    if problem_dir.exists():
        raise StartError(f"Problem directory already exists: {problem_dir}")

    problem_dir.mkdir(parents=True, exist_ok=True)
    (problem_dir / "link.txt").write_text(f"{url}\n")

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
        match = re.fullmatch(r"https?://codeforces\.com/gym/([0-9]+)/problem/([^/?#]+)/?", url)
    if not match:
        raise StartError(
            "Invalid Codeforces problem URL "
            "(expected .../contest/<id>/problem/<index>, "
            ".../problemset/problem/<id>/<index>, or .../gym/<id>/problem/<index>): "
            f"{url}"
        )

    contest_id = int(match.group(1))
    problem_index = match.group(2).lower()
    title = codeforces_problem_title(contest_id, problem_index, url)

    if not title:
        raise StartError(f"Failed to extract Codeforces title from: {url}")

    return f"{contest_id}-{problem_index}-{slug_hyphen(title)}"


def codeforces_problem_title(contest_id: int, problem_index: str, url: str) -> str:
    title = ""
    api_urls = (
        f"https://codeforces.com/api/contest.standings?contestId={contest_id}",
        "https://codeforces.com/api/problemset.problems",
    )

    for api_url in api_urls:
        try:
            data = json.loads(fetch_text(api_url))
        except (StartError, json.JSONDecodeError):
            continue

        problems = data.get("result", {}).get("problems", [])
        for problem in problems:
            if (
                problem.get("contestId") == contest_id
                and problem.get("index", "").upper() == problem_index.upper()
            ):
                title = problem["name"]
                break

        if title:
            break

    if not title:
        title = codeforces_page_title(url)

    if not title:
        mirror_url = url.replace("https://codeforces.com/", "https://mirror.codeforces.com/")
        mirror_url = mirror_url.replace("http://codeforces.com/", "https://mirror.codeforces.com/")
        title = codeforces_page_title(mirror_url)

    if not title:
        title = codeforces_contest_table_title(contest_id, problem_index, url)

    return title


def clean_codeforces_title(title: str) -> str:
    title = re.sub(r"<[^>]+>", "", title)
    title = re.sub(r"^[A-Z0-9]+\.\s*", "", html.unescape(title))
    return re.sub(r"\s+", " ", title).strip()


def codeforces_page_title(url: str) -> str:
    try:
        page = fetch_text(url)
    except StartError:
        return ""

    title_match = re.search(
        r'<div[^>]*class="[^"]*\btitle\b[^"]*"[^>]*>\s*(.*?)\s*</div>',
        page,
        re.I | re.S,
    )
    if not title_match:
        return ""

    return clean_codeforces_title(title_match.group(1))


def codeforces_contest_table_title(contest_id: int, problem_index: str, url: str) -> str:
    kind_match = re.search(r"codeforces\.com/(contest|gym)/", url)
    if not kind_match:
        return ""

    kind = kind_match.group(1)
    problem_path = f"/{kind}/{contest_id}/problem/{problem_index.upper()}"
    contest_url = f"https://mirror.codeforces.com/{kind}/{contest_id}"

    try:
        page = fetch_text(contest_url)
    except StartError:
        return ""

    link_matches = re.findall(
        rf'href="{re.escape(problem_path)}"[^>]*>\s*(?:<!--.*?-->\s*)?(.+?)\s*(?:<!--.*?-->\s*)?</a>',
        page,
        re.I | re.S,
    )
    for link_text in link_matches:
        title = clean_codeforces_title(link_text)
        if title and title.upper() != problem_index.upper():
            return title

    return ""


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


def parse_kattis(url: str) -> str:
    match = re.fullmatch(r"https?://open\.kattis\.com/problems/([^/?#]+)/?", url)
    if not match:
        raise StartError(
            f"Invalid Kattis problem URL (expected https://open.kattis.com/problems/<problem_id>): {url}"
        )

    return match.group(1).lower().replace("_", "-")


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
    "kattis": parse_kattis,
    "usaco": parse_usaco,
    "yosupo": parse_yosupo,
}


def print_usage(program: str, platform: str, file=sys.stdout) -> None:
    label = platform.replace("_", " ").title()
    print(f"Usage: {program} [--cpp|--py|--hs] <{label} problem url>", file=file)


def main(argv: list[str]) -> int:
    invoked = Path(argv[0])
    platform_dir = (Path.cwd() / invoked.parent).resolve() if not invoked.is_absolute() else invoked.parent.resolve()
    repo_root = platform_dir.parent
    platform = platform_dir.name

    if len(argv) == 2 and argv[1] in ("-h", "--help"):
        print_usage(argv[0], platform)
        return 0

    if len(argv) == 2:
        template = LANGUAGE_TEMPLATES["--cpp"]
        url = argv[1]
    elif len(argv) == 3:
        language_flag = argv[1]
        template = LANGUAGE_TEMPLATES.get(language_flag)
        if template is None:
            print_usage(argv[0], platform, file=sys.stderr)
            return 1
        url = argv[2]
    else:
        print_usage(argv[0], platform, file=sys.stderr)
        return 1
    try:
        if platform == "project_euler":
            dirname, description = parse_project_euler(url)
            create_problem(platform_dir, repo_root, dirname, url, template)
            (platform_dir / dirname / "description.md").write_text(description)
        else:
            parser = PARSERS.get(platform)
            if parser is None:
                raise StartError(f"Unsupported platform directory: {platform}")
            dirname = parser(url)
            create_problem(platform_dir, repo_root, dirname, url, template)
    except StartError as exc:
        print(exc, file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
