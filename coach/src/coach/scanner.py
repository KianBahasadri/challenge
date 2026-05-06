from __future__ import annotations

from datetime import datetime
from pathlib import Path

from .models import PlatformStats, Problem, WorkspaceStats

SOLVED_MARKERS = ("completed", "submission.txt")
IGNORED_PLATFORM_DIRS = {".git", ".venv", "__pycache__", "coach"}


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
            problems.append(_problem_from_dir(platform_dir.name, problem_dir, link_path))

    return tuple(problems)


def build_stats(workspace: Path) -> WorkspaceStats:
    problems = scan_workspace(workspace)
    return WorkspaceStats(
        workspace=workspace.resolve(),
        problems=problems,
        platforms=_platform_stats(problems),
    )


def _scan_nested_platform(platform_dir: Path, platform_name: str) -> list[Problem]:
    problems: list[Problem] = []
    for link_path in sorted(platform_dir.rglob("link.txt"), key=lambda path: path.parent.as_posix().lower()):
        problem_dir = link_path.parent
        relative_name = problem_dir.relative_to(platform_dir).as_posix()
        problems.append(_problem_from_dir(platform_name, problem_dir, link_path, relative_name))
    return problems


def _problem_from_dir(platform: str, problem_dir: Path, link_path: Path, name: str | None = None) -> Problem:
    started_at = _started_at(problem_dir)
    return Problem(
        platform=platform,
        name=name or problem_dir.name,
        path=problem_dir,
        solved=any((problem_dir / marker).exists() for marker in SOLVED_MARKERS),
        link=_read_link(link_path),
        started_at=started_at,
        started_on=_format_started_on(started_at),
    )


def _platform_stats(problems: tuple[Problem, ...]) -> tuple[PlatformStats, ...]:
    grouped: dict[str, list[Problem]] = {}
    for problem in problems:
        grouped.setdefault(problem.platform, []).append(problem)

    stats = [
        PlatformStats(
            name=platform,
            solved=sum(problem.solved for problem in platform_problems),
            total=len(platform_problems),
        )
        for platform, platform_problems in grouped.items()
    ]
    return tuple(sorted(stats, key=lambda stat: (-stat.solved, -stat.total, stat.name.lower())))


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
