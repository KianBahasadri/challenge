from __future__ import annotations

import argparse
import shlex
import sys
from pathlib import Path

from .llm import (
    build_coaching_prompt,
    default_chat_prompt,
    interactive_command_for_agent,
    run_interactive_agent,
)
from .models import Problem, WorkspaceStats
from .scanner import build_stats, default_workspace


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Observe and coach a competitive-programming workspace.")
    parser.add_argument("--workspace", type=Path, default=default_workspace(), help="Competitive-programming workspace root.")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("summary", help="Print workspace progress counts.")

    list_parser = subparsers.add_parser("list", help="List detected problems.")
    solved_group = list_parser.add_mutually_exclusive_group()
    solved_group.add_argument("--solved", action="store_true", help="Only show solved problems.")
    solved_group.add_argument("--unsolved", action="store_true", help="Only show unsolved problems.")
    list_parser.add_argument("--platform", help="Only show one platform.")
    list_parser.add_argument("--limit", type=int, help="Maximum number of problems to print.")

    recent_parser = subparsers.add_parser("recent", help="List recently started problems.")
    recent_parser.add_argument("--limit", type=int, default=10, help="Maximum number of problems to print.")

    chat_parser = subparsers.add_parser("chat", help="Start an interactive local LLM coaching session.")
    chat_parser.add_argument("prompt", nargs="*", help="Optional opening coaching request.")
    chat_parser.add_argument("--agent", choices=("opencode", "codex"), default="opencode", help="Local CLI to run.")
    chat_parser.add_argument("--context-limit", type=int, default=20, help="Number of problems to include in prompt samples.")
    chat_parser.add_argument("--dry-run", action="store_true", help="Print the delegated command and prompt without starting the chat.")

    args = parser.parse_args(argv)
    if args.command is None:
        parser.print_help()
        return

    stats = build_stats(args.workspace)
    if args.command == "summary":
        print_summary(stats)
        return
    if args.command == "list":
        print_problem_list(stats.problems, solved=args.solved, unsolved=args.unsolved, platform=args.platform, limit=args.limit)
        return
    if args.command == "recent":
        recent = sorted(stats.problems, key=lambda problem: problem.started_at or 0, reverse=True)
        print_problem_list(tuple(recent), limit=args.limit)
        return
    if args.command == "chat":
        user_prompt = " ".join(args.prompt) if args.prompt else default_chat_prompt()
        prompt = build_coaching_prompt(stats, user_prompt, args.context_limit)
        if args.dry_run:
            command = interactive_command_for_agent(args.agent, prompt, stats.workspace)
            print("Command:")
            print(shlex.join(command))
            print("\nPrompt:")
            print(prompt)
            return
        try:
            raise SystemExit(run_interactive_agent(args.agent, prompt, stats.workspace))
        except FileNotFoundError as error:
            print(f"coach: {error}", file=sys.stderr)
            raise SystemExit(127) from error


def print_summary(stats: WorkspaceStats) -> None:
    print(f"Workspace: {stats.workspace}")
    print(f"Solved:    {_format_progress(stats.solved, stats.total, stats.percent)}")
    print(f"Unsolved:  {stats.unsolved}")
    if not stats.platforms:
        return

    name_width = max(len(platform.name) for platform in stats.platforms)
    solved_width = max(len(str(platform.solved)) for platform in stats.platforms)
    total_width = max(len(str(platform.total)) for platform in stats.platforms)
    percent_width = max(len(f"{platform.percent:.0f}") for platform in stats.platforms)
    for platform in stats.platforms:
        print(
            f"{platform.name:<{name_width}}  "
            f"{platform.solved:>{solved_width}}/{platform.total:>{total_width}}  "
            f"({platform.percent:>{percent_width}.0f}%)"
        )


def _format_progress(solved: int, total: int, percent: float) -> str:
    return f"{solved}/{total} ({percent:.0f}%)"


def print_problem_list(
    problems: tuple[Problem, ...],
    *,
    solved: bool = False,
    unsolved: bool = False,
    platform: str | None = None,
    limit: int | None = None,
) -> None:
    filtered = list(problems)
    if solved:
        filtered = [problem for problem in filtered if problem.solved]
    if unsolved:
        filtered = [problem for problem in filtered if not problem.solved]
    if platform:
        filtered = [problem for problem in filtered if problem.platform == platform]
    if limit is not None:
        filtered = filtered[:limit]

    for problem in filtered:
        status = "solved" if problem.solved else "unsolved"
        started = f" started={problem.started_on}" if problem.started_on else ""
        print(f"{problem.key} [{status}]{started}")
