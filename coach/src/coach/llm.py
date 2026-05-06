from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from .models import WorkspaceStats


def build_coaching_prompt(stats: WorkspaceStats, user_prompt: str, limit: int = 20) -> str:
    unsolved = [problem for problem in stats.problems if not problem.solved]
    recent = sorted(
        stats.problems,
        key=lambda problem: problem.started_at or 0,
        reverse=True,
    )[:limit]

    lines = [
        "You are a competitive-programming coach.",
        "Give concise coaching. Prefer hints, edge cases, complexity checks, and next practice suggestions.",
        "Do not provide full solutions unless explicitly asked.",
        "",
        f"Workspace: {stats.workspace}",
        f"Progress: {stats.solved}/{stats.total} solved ({stats.percent:.0f}%), {stats.unsolved} unsolved",
        "",
        "Platforms:",
    ]
    lines.extend(f"- {platform.name}: {platform.solved}/{platform.total} solved" for platform in stats.platforms)
    lines.extend(["", f"Unsolved sample ({min(limit, len(unsolved))}/{len(unsolved)}):"])
    lines.extend(f"- {problem.key}" for problem in unsolved[:limit])
    lines.extend(["", f"Recent sample ({len(recent)}):"])
    lines.extend(f"- {problem.key}: {'solved' if problem.solved else 'unsolved'}" for problem in recent)
    lines.extend(["", "User request:", user_prompt])
    return "\n".join(lines)


def default_chat_prompt() -> str:
    return "Start an interactive coaching session. Ask what I am working on, then coach with hints and checks."


def interactive_command_for_agent(agent: str, prompt: str, workspace: Path) -> list[str]:
    if agent == "opencode":
        return ["opencode", str(workspace), "--prompt", prompt]
    if agent == "codex":
        return ["codex", "--cd", str(workspace), prompt]
    raise ValueError(f"unsupported agent: {agent}")


def run_interactive_agent(agent: str, prompt: str, workspace: Path) -> int:
    executable = shutil.which(agent)
    if executable is None:
        raise FileNotFoundError(f"Could not find {agent!r} on PATH")
    command = interactive_command_for_agent(agent, prompt, workspace)
    return subprocess.run(command, cwd=workspace, check=False).returncode
