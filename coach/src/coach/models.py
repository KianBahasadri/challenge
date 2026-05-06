from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Problem:
    platform: str
    name: str
    path: Path
    solved: bool
    link: str | None = None
    started_at: float | None = None
    started_on: str | None = None

    @property
    def key(self) -> str:
        return f"{self.platform}/{self.name}"


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
class WorkspaceStats:
    workspace: Path
    problems: tuple[Problem, ...]
    platforms: tuple[PlatformStats, ...]

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
