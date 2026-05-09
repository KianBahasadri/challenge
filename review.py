#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path


class ReviewError(Exception):
    pass


LANGUAGES = {
    ".c": "c",
    ".cc": "cpp",
    ".cpp": "cpp",
    ".cxx": "cpp",
    ".hs": "haskell",
    ".py": "python",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a post-AC review.md for a solved problem from an accepted code file."
    )
    parser.add_argument("code_file", help="path to the accepted solution file")
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite an existing review.md",
    )
    return parser.parse_args()


def read_optional(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text().strip()


def code_fence(code: str, suffix: str) -> str:
    language = LANGUAGES.get(suffix.lower(), "")
    longest_backtick_run = 0
    current_run = 0

    for char in code:
        if char == "`":
            current_run += 1
            longest_backtick_run = max(longest_backtick_run, current_run)
        else:
            current_run = 0

    fence = "`" * max(3, longest_backtick_run + 1)
    return f"{fence}{language}\n{code.rstrip()}\n{fence}"


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise ReviewError(f"Template is missing expected placeholder: {old!r}")
    return text.replace(old, new, 1)


def build_review(template: str, problem_dir: Path, code_file: Path) -> str:
    link = read_optional(problem_dir / "link.txt") or "Paste the statement/link here."
    code = code_file.read_text()

    review = template
    review = replace_once(
        review,
        "review-date: # YYYY-MM-DD",
        f"review-date: {date.today().isoformat()} # YYYY-MM-DD",
    )
    review = replace_once(review, "Paste the statement/link here.", link)
    review = replace_once(
        review,
        "Paste the accepted code here.",
        code_fence(code, code_file.suffix),
    )
    return review


def create_review(code_file: Path, force: bool) -> Path:
    repo_root = Path(__file__).resolve().parent
    template_path = repo_root / "review.md"

    if not template_path.exists():
        raise ReviewError(f"Missing review template: {template_path}")

    code_file = code_file.expanduser().resolve()
    if not code_file.exists():
        raise ReviewError(f"Code file does not exist: {code_file}")
    if not code_file.is_file():
        raise ReviewError(f"Expected a code file, got: {code_file}")

    problem_dir = code_file.parent
    if not (problem_dir / "submission.txt").exists() and not (problem_dir / "completed").exists():
        raise ReviewError(
            f"Problem does not look solved yet: missing submission.txt or completed in {problem_dir}"
        )

    output_path = problem_dir / "review.md"
    if output_path.exists() and not force:
        raise ReviewError(f"Review already exists: {output_path} (use --force to overwrite)")

    review = build_review(template_path.read_text(), problem_dir, code_file)
    output_path.write_text(review)
    return output_path


def main() -> int:
    args = parse_args()
    try:
        output_path = create_review(Path(args.code_file), args.force)
    except ReviewError as exc:
        print(exc)
        return 1

    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
