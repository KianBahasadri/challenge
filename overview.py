#!/usr/bin/env python3
import argparse
from collections import Counter
import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "overview.json"
CODEFORCES_API = "https://codeforces.com/api/problemset.problems"
USACO_GUIDE_ZIP = "https://codeload.github.com/cpinitiative/usaco-guide/zip/refs/heads/master"
# Cache stable facts: once a problem is solved, normal runs keep it solved, and
# Codeforces ratings, USACO divisions, and Codewars kyu are reused after first
# lookup. Volatile totals, like the current number of link.txt problem dirs,
# are rescanned.


def scan_overview():
    problem_dirs = sorted(
        link.parent
        for link in ROOT.rglob("link.txt")
        if not any(part.startswith(".") for part in link.relative_to(ROOT).parts)
    )
    cache = load_cache()
    solved_dirs = set(cache["solved_dirs"])
    problem_names = {str(d.relative_to(ROOT)) for d in problem_dirs}

    for d in problem_dirs:
        name = str(d.relative_to(ROOT))
        if name not in solved_dirs and ((d / "submission.txt").is_file() or (d / "completed").is_file()):
            solved_dirs.add(name)

    cache["solved_dirs"] = solved_dirs
    save_cache(cache)
    return {"problems": len(problem_dirs), "solved": len(solved_dirs & problem_names)}


def load_cache():
    if not CACHE.exists():
        return {
            "solved_dirs": [],
            "codeforces_ratings": {},
            "usaco_levels": {},
            "usaco_guide_difficulties": {},
            "codewars_kyu": {},
        }
    with CACHE.open() as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError("invalid cache")
    solved_dirs = data.get("solved_dirs", data.get("completed", []))
    if not isinstance(solved_dirs, list) or not all(isinstance(d, str) for d in solved_dirs):
        raise ValueError("missing solved dirs")
    codeforces_ratings = data.get("codeforces_ratings", {})
    if not isinstance(codeforces_ratings, dict) or not all(
        isinstance(k, str) and (isinstance(v, int) or v is None) for k, v in codeforces_ratings.items()
    ):
        raise ValueError("invalid Codeforces ratings")
    usaco_levels = data.get("usaco_levels", {})
    if not isinstance(usaco_levels, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in usaco_levels.items()
    ):
        raise ValueError("invalid USACO levels")
    usaco_guide_difficulties = data.get("usaco_guide_difficulties", {})
    if not isinstance(usaco_guide_difficulties, dict) or not all(
        isinstance(k, str) and isinstance(v, str) for k, v in usaco_guide_difficulties.items()
    ):
        raise ValueError("invalid USACO Guide difficulties")
    codewars_kyu = data.get("codewars_kyu", {})
    if not isinstance(codewars_kyu, dict) or not all(
        isinstance(k, str) and isinstance(v, int) for k, v in codewars_kyu.items()
    ):
        raise ValueError("invalid Codewars kyu")
    return {
        "solved_dirs": solved_dirs,
        "codeforces_ratings": codeforces_ratings,
        "usaco_levels": usaco_levels,
        "usaco_guide_difficulties": usaco_guide_difficulties,
        "codewars_kyu": codewars_kyu,
    }


def save_cache(data):
    tmp = CACHE.with_suffix(".json.tmp")
    with tmp.open("w") as f:
        json.dump(
            {
                "solved_dirs": sorted(data.get("solved_dirs", [])),
                "codeforces_ratings": dict(sorted(data.get("codeforces_ratings", {}).items())),
                "usaco_levels": dict(sorted(data.get("usaco_levels", {}).items())),
                "usaco_guide_difficulties": dict(sorted(data.get("usaco_guide_difficulties", {}).items())),
                "codewars_kyu": dict(sorted(data.get("codewars_kyu", {}).items())),
            },
            f,
            indent=2,
        )
        f.write("\n")
    tmp.replace(CACHE)


def codeforces_problem_dirs():
    cf_root = ROOT / "codeforces"
    if not cf_root.is_dir():
        return []
    return sorted(
        link.parent
        for link in cf_root.rglob("link.txt")
        if not any(part.startswith(".") for part in link.relative_to(ROOT).parts)
    )


def codeforces_key(link):
    match = re.search(r"/problemset/problem/(\d+)/([^/?#]+)", link)
    if not match:
        match = re.search(r"/contest/(\d+)/problem/([^/?#]+)", link)
    if not match:
        return None
    return int(match.group(1)), match.group(2)


def fetch_codeforces_ratings():
    raw = subprocess.check_output(
        ["curl", "-fsSL", "--max-time", "20", CODEFORCES_API],
        stderr=subprocess.DEVNULL,
        text=True,
    )
    data = json.loads(raw)
    ratings = {}
    for p in data["result"]["problems"]:
        if "rating" in p:
            ratings[(p["contestId"], p["index"])] = p["rating"]
    return ratings


def codeforces_rating_counts():
    dirs = codeforces_problem_dirs()
    if not dirs:
        return Counter()

    cache = load_cache()
    cached_ratings = cache["codeforces_ratings"]
    solved_dirs = set(cache["solved_dirs"])
    missing = []
    for d in dirs:
        name = str(d.relative_to(ROOT))
        link = (d / "link.txt").read_text().strip()
        if name not in cached_ratings:
            missing.append((name, codeforces_key(link)))

    if missing:
        fetched = True
        try:
            ratings = fetch_codeforces_ratings()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError, KeyError):
            fetched = False
            ratings = {}
        if fetched:
            for name, key in missing:
                cached_ratings[name] = ratings.get(key) if key is not None else None
            cache["codeforces_ratings"] = cached_ratings
            save_cache(cache)

    counts = Counter()
    for d in dirs:
        name = str(d.relative_to(ROOT))
        if name in solved_dirs:
            rating = cached_ratings.get(name)
            counts[rating if rating is not None else "unknown"] += 1
    return counts


def usaco_problem_dirs():
    usaco_root = ROOT / "usaco"
    if not usaco_root.is_dir():
        return []
    return sorted(
        link.parent
        for link in usaco_root.rglob("link.txt")
        if not any(part.startswith(".") for part in link.relative_to(ROOT).parts)
    )


def fetch_usaco_level(link):
    raw = subprocess.check_output(
        ["curl", "-fsSL", "--max-time", "20", link],
        stderr=subprocess.DEVNULL,
        text=True,
    )
    match = re.search(r"USACO [^<\n]+ Contest,\s*(Bronze|Silver|Gold|Platinum)", raw, re.IGNORECASE)
    if match:
        return match.group(1).lower()
    return None


def usaco_id(link):
    match = re.search(r"[?&]cpid=(\d+)", link)
    if not match:
        return None
    return f"usaco-{match.group(1)}"


def collect_usaco_guide_difficulties(value, difficulties):
    if isinstance(value, dict):
        unique_id = value.get("uniqueId")
        difficulty = value.get("difficulty")
        if isinstance(unique_id, str) and unique_id.startswith("usaco-") and isinstance(difficulty, str):
            difficulties[unique_id] = difficulty.lower()
        for child in value.values():
            collect_usaco_guide_difficulties(child, difficulties)
    elif isinstance(value, list):
        for child in value:
            collect_usaco_guide_difficulties(child, difficulties)


def fetch_usaco_guide_difficulties(wanted_ids):
    difficulties = {}
    with tempfile.NamedTemporaryFile(suffix=".zip") as tmp:
        subprocess.check_call(
            ["curl", "-L", "-fsS", "--max-time", "60", "-o", tmp.name, USACO_GUIDE_ZIP],
            stderr=subprocess.DEVNULL,
        )
        with zipfile.ZipFile(tmp.name) as z:
            for name in z.namelist():
                if "/content/" not in name or not name.endswith(".problems.json"):
                    continue
                collect_usaco_guide_difficulties(json.loads(z.read(name)), difficulties)
                if wanted_ids <= difficulties.keys():
                    break

    return difficulties


def usaco_level_counts():
    dirs = usaco_problem_dirs()
    if not dirs:
        return Counter(), Counter()

    cache = load_cache()
    solved_dirs = set(cache["solved_dirs"])
    levels = cache["usaco_levels"]
    guide_difficulties = cache["usaco_guide_difficulties"]
    missing = [d for d in dirs if str(d.relative_to(ROOT)) not in levels]

    changed = False
    for d in missing:
        name = str(d.relative_to(ROOT))
        link = (d / "link.txt").read_text().strip()
        try:
            level = fetch_usaco_level(link)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            level = None
        if level is not None:
            levels[name] = level
            changed = True

    if changed:
        cache["usaco_levels"] = levels
        save_cache(cache)

    missing_difficulties = []
    for d in dirs:
        name = str(d.relative_to(ROOT))
        uid = usaco_id((d / "link.txt").read_text().strip())
        if uid is not None and name not in guide_difficulties:
            missing_difficulties.append((name, uid))

    if missing_difficulties:
        try:
            by_id = fetch_usaco_guide_difficulties({uid for _, uid in missing_difficulties})
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError, KeyError):
            by_id = {}
        changed = False
        for name, uid in missing_difficulties:
            difficulty = by_id.get(uid)
            if difficulty is not None:
                guide_difficulties[name] = difficulty
                changed = True
        if changed:
            cache["usaco_guide_difficulties"] = guide_difficulties
            save_cache(cache)

    level_counts = Counter()
    difficulty_counts = Counter()
    for d in dirs:
        name = str(d.relative_to(ROOT))
        if name in solved_dirs:
            level_counts[levels.get(name, "unknown")] += 1
            difficulty_counts[guide_difficulties.get(name, "unknown")] += 1

    return level_counts, difficulty_counts


def codewars_problem_dirs():
    codewars_root = ROOT / "codewars"
    if not codewars_root.is_dir():
        return []
    return sorted(
        link.parent
        for link in codewars_root.rglob("link.txt")
        if not any(part.startswith(".") for part in link.relative_to(ROOT).parts)
    )


def codewars_kata_id(link):
    match = re.search(r"/kata/([^/?#]+)", link)
    if not match:
        return None
    return match.group(1)


def fetch_codewars_kyu(kata_id):
    raw = subprocess.check_output(
        ["curl", "-fsSL", "--max-time", "20", f"https://www.codewars.com/api/v1/code-challenges/{kata_id}"],
        stderr=subprocess.DEVNULL,
        text=True,
    )
    data = json.loads(raw)
    rank_id = data.get("rank", {}).get("id")
    if isinstance(rank_id, int) and rank_id < 0:
        return -rank_id
    return None


def codewars_kyu_counts():
    dirs = codewars_problem_dirs()
    if not dirs:
        return Counter(), []

    cache = load_cache()
    solved_dirs = set(cache["solved_dirs"])
    kyu = cache["codewars_kyu"]
    missing = [d for d in dirs if str(d.relative_to(ROOT)) not in kyu]

    changed = False
    for d in missing:
        name = str(d.relative_to(ROOT))
        kata_id = codewars_kata_id((d / "link.txt").read_text().strip())
        if kata_id is None:
            continue
        try:
            value = fetch_codewars_kyu(kata_id)
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, json.JSONDecodeError):
            value = None
        if value is not None:
            kyu[name] = value
            changed = True

    if changed:
        cache["codewars_kyu"] = kyu
        save_cache(cache)

    counts = Counter()
    unknown = []
    for d in dirs:
        name = str(d.relative_to(ROOT))
        if name in solved_dirs:
            if name in kyu:
                counts[kyu[name]] += 1
            else:
                counts["unknown"] += 1
                unknown.append(name)

    return counts, unknown


def print_bucket(label, count):
    print(f"  {label:<8} {count}")


def print_sub_bucket(label, count):
    print(f"    {label:<8} {count}")


def print_summary(data):
    print(f"Problems: {data['problems']}")
    print(f"Solved:   {data['solved']}")
    print()

    cf_counts = codeforces_rating_counts()
    if cf_counts:
        print(f"Codeforces {sum(cf_counts.values())}")
        for rating in sorted(k for k in cf_counts if k != "unknown"):
            print_bucket(str(rating), cf_counts[rating])
        if "unknown" in cf_counts:
            print_bucket("Unknown", cf_counts["unknown"])

    usaco_counts, usaco_difficulty_counts = usaco_level_counts()
    if usaco_counts:
        print()
        print(f"USACO {sum(usaco_counts.values())}")
        for level in ("bronze", "silver", "gold", "platinum"):
            if level in usaco_counts:
                print_bucket(level.title(), usaco_counts[level])
        if "unknown" in usaco_counts:
            print_bucket("Unknown", usaco_counts["unknown"])
        for difficulty in ("very easy", "easy", "normal", "hard", "very hard"):
            if difficulty in usaco_difficulty_counts:
                print_sub_bucket(difficulty.title(), usaco_difficulty_counts[difficulty])
        if "unknown" in usaco_difficulty_counts:
            print_sub_bucket("Unknown", usaco_difficulty_counts["unknown"])

    codewars_counts, unknown_codewars = codewars_kyu_counts()
    if codewars_counts:
        print()
        print(f"Codewars {sum(codewars_counts.values())}")
        for kyu in sorted(k for k in codewars_counts if k != "unknown"):
            print_bucket(f"{kyu} kyu", codewars_counts[kyu])
        if "unknown" in codewars_counts:
            print_bucket("Unknown", codewars_counts["unknown"])
            print()
            print("Missing Codewars kyu")
            for name in unknown_codewars:
                print(f"  {name}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--force", action="store_true", help="rescan problem files")
    args = parser.parse_args()

    if args.force:
        save_cache(
            {
                "solved_dirs": [],
                "codeforces_ratings": {},
                "usaco_levels": {},
                "usaco_guide_difficulties": {},
                "codewars_kyu": {},
            }
        )
        data = scan_overview()
    else:
        try:
            data = scan_overview()
        except (OSError, ValueError, json.JSONDecodeError):
            save_cache(
                {
                    "solved_dirs": [],
                    "codeforces_ratings": {},
                    "usaco_levels": {},
                    "usaco_guide_difficulties": {},
                    "codewars_kyu": {},
                }
            )
            data = scan_overview()

    print_summary(data)


if __name__ == "__main__":
    main()
