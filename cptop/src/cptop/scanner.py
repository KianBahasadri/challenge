from __future__ import annotations

from pathlib import Path

from .models import Problem

SOLVED_MARKERS = ("completed", "submission.txt")
IGNORED_PLATFORM_DIRS = {".git", ".venv", "cptop", "__pycache__"}


def default_workspace() -> Path:
    return Path(__file__).resolve().parents[3]


def scan_workspace(workspace: Path) -> tuple[Problem, ...]:
    workspace = workspace.resolve()
    problems: list[Problem] = []

    for platform_dir in sorted(workspace.iterdir(), key=lambda path: path.name.lower()):
        if not platform_dir.is_dir() or platform_dir.name in IGNORED_PLATFORM_DIRS:
            continue
        if platform_dir.name.startswith("."):
            continue

        for problem_dir in sorted(platform_dir.iterdir(), key=lambda path: path.name.lower()):
            if not problem_dir.is_dir():
                continue
            link_path = problem_dir / "link.txt"
            if not link_path.exists():
                continue

            solved = any((problem_dir / marker).exists() for marker in SOLVED_MARKERS)
            problems.append(
                Problem(
                    platform=platform_dir.name,
                    name=problem_dir.name,
                    path=problem_dir,
                    solved=solved,
                    link=_read_link(link_path),
                )
            )

    return tuple(problems)


def _read_link(path: Path) -> str | None:
    try:
        value = path.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return value or None
