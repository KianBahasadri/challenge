from __future__ import annotations

from datetime import datetime
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

        if platform_dir.name == "usaco.guide":
            problems.extend(_scan_nested_platform(platform_dir, "usaco"))
            continue

        for problem_dir in sorted(platform_dir.iterdir(), key=lambda path: path.name.lower()):
            if not problem_dir.is_dir():
                continue
            link_path = problem_dir / "link.txt"
            if not link_path.exists():
                continue

            solved = any((problem_dir / marker).exists() for marker in SOLVED_MARKERS)
            started_at = _started_at(problem_dir)
            problems.append(
                Problem(
                    platform=platform_dir.name,
                    name=problem_dir.name,
                    path=problem_dir,
                    solved=solved,
                    link=_read_link(link_path),
                    started_on=_format_started_on(started_at),
                    started_at=started_at,
                )
            )

    return tuple(problems)


def _scan_nested_platform(platform_dir: Path, platform_name: str) -> list[Problem]:
    problems: list[Problem] = []
    for link_path in sorted(platform_dir.rglob("link.txt"), key=lambda path: path.parent.as_posix().lower()):
        problem_dir = link_path.parent
        relative_name = problem_dir.relative_to(platform_dir).as_posix()
        solved = any((problem_dir / marker).exists() for marker in SOLVED_MARKERS)
        started_at = _started_at(problem_dir)
        problems.append(
            Problem(
                platform=platform_name,
                name=relative_name,
                path=problem_dir,
                solved=solved,
                link=_read_link(link_path),
                started_on=_format_started_on(started_at),
                started_at=started_at,
            )
        )
    return problems


def _read_link(path: Path) -> str | None:
    try:
        value = path.read_text(encoding="utf-8").strip()
    except OSError:
        return None
    return value or None


def _started_at(path: Path) -> float | None:
    try:
        stat = path.stat()
    except OSError:
        return None
    return getattr(stat, "st_birthtime", stat.st_ctime)


def _format_started_on(timestamp: float | None) -> str | None:
    if timestamp is None:
        return None
    return datetime.fromtimestamp(timestamp).strftime("%b %-d")
