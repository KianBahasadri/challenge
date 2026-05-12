#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path


def print_usage(program: str) -> None:
    print(f"Usage: {program} [--open]")


def main(argv: list[str]) -> int:
    if any(arg in ("-h", "--help") for arg in argv[1:]):
        print_usage(argv[0])
        return 0

    script_dir = Path(argv[0]).absolute().parent
    open_links = "--open" in argv[1:]

    for d in sorted(script_dir.iterdir()):
        if d.name.startswith(".") or not d.is_dir():
            continue

        if not (d / "submission.txt").is_file() and not (d / "completed").is_file():
            print(d.name)
            link = d / "link.txt"
            if open_links and link.is_file():
                subprocess.run(["firefox", link.read_text().strip()], check=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
