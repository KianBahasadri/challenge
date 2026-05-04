from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .models import DashboardStats, PlatformStats, Problem, ProblemTags, TagStats


def default_tag_file() -> Path:
    return Path(__file__).resolve().parents[2] / "data" / "problem_tags.json"


def load_tags(path: Path) -> tuple[dict[str, ProblemTags], tuple[str, ...]]:
    if not path.exists():
        return {}, (f"Tag file does not exist: {path}",)

    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return {}, (f"Could not load tags from {path}: {error}",)

    if not isinstance(raw, dict):
        return {}, (f"Tag file must contain a JSON object: {path}",)

    tags: dict[str, ProblemTags] = {}
    warnings: list[str] = []
    for key, value in raw.items():
        if not isinstance(key, str) or not isinstance(value, dict):
            warnings.append(f"Skipping invalid tag entry: {key}")
            continue
        parsed = _parse_problem_tags(value)
        tags[key] = parsed

    return tags, tuple(warnings)


def build_dashboard_stats(
    problems: tuple[Problem, ...],
    workspace: Path,
    tag_file: Path,
) -> DashboardStats:
    tag_map, warnings = load_tags(tag_file)
    return DashboardStats(
        problems=problems,
        platform_stats=_platform_stats(problems),
        tag_stats=_tag_stats(problems, tag_map),
        missing_tag_keys=_missing_tag_keys(problems, tag_map),
        tag_count=len(tag_map),
        workspace=workspace,
        tag_file=tag_file,
        warnings=warnings,
    )


def _parse_problem_tags(value: dict[str, Any]) -> ProblemTags:
    raw_tags = value.get("tags", [])
    tags = tuple(str(tag).strip() for tag in raw_tags if str(tag).strip()) if isinstance(raw_tags, list) else ()
    difficulty = value.get("difficulty")
    notes = value.get("notes")
    return ProblemTags(
        tags=tags,
        difficulty=str(difficulty) if difficulty is not None else None,
        notes=str(notes) if notes is not None else None,
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
    return tuple(sorted(stats, key=lambda stat: (-stat.total, stat.name.lower())))


def _tag_stats(problems: tuple[Problem, ...], tag_map: dict[str, ProblemTags]) -> tuple[TagStats, ...]:
    grouped: dict[str, list[Problem]] = {}
    for problem in problems:
        for tag in tag_map.get(problem.key, ProblemTags()).tags:
            grouped.setdefault(tag, []).append(problem)

    stats = [
        TagStats(
            name=tag,
            solved=sum(problem.solved for problem in tagged_problems),
            total=len(tagged_problems),
        )
        for tag, tagged_problems in grouped.items()
    ]
    return tuple(sorted(stats, key=lambda stat: (stat.percent, -stat.total, stat.name.lower())))


def _missing_tag_keys(problems: tuple[Problem, ...], tag_map: dict[str, ProblemTags]) -> tuple[str, ...]:
    return tuple(sorted(problem.key for problem in problems if problem.solved and not tag_map.get(problem.key, ProblemTags()).tags))
