from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Problem:
    platform: str
    name: str
    path: Path
    solved: bool
    link: str | None = None

    @property
    def key(self) -> str:
        return f"{self.platform}/{self.name}"


@dataclass(frozen=True)
class ProblemTags:
    tags: tuple[str, ...] = ()
    difficulty: str | None = None
    notes: str | None = None


@dataclass(frozen=True)
class PlatformStats:
    name: str
    solved: int
    total: int

    @property
    def unsolved(self) -> int:
        return self.total - self.solved

    @property
    def percent(self) -> float:
        if self.total == 0:
            return 0.0
        return self.solved / self.total * 100


@dataclass(frozen=True)
class TagStats:
    name: str
    solved: int = 0
    total: int = 0

    @property
    def unsolved(self) -> int:
        return self.total - self.solved

    @property
    def percent(self) -> float:
        if self.total == 0:
            return 0.0
        return self.solved / self.total * 100


@dataclass(frozen=True)
class DashboardStats:
    problems: tuple[Problem, ...]
    platform_stats: tuple[PlatformStats, ...]
    tag_stats: tuple[TagStats, ...]
    missing_tag_keys: tuple[str, ...]
    tag_count: int
    workspace: Path
    tag_file: Path
    warnings: tuple[str, ...] = field(default_factory=tuple)

    @property
    def solved(self) -> int:
        return sum(problem.solved for problem in self.problems)

    @property
    def total(self) -> int:
        return len(self.problems)

    @property
    def unsolved(self) -> int:
        return self.total - self.solved

    @property
    def percent(self) -> float:
        if self.total == 0:
            return 0.0
        return self.solved / self.total * 100
