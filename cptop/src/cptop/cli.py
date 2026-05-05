from __future__ import annotations

import argparse
from pathlib import Path

from .app import CptopApp
from .scanner import default_workspace, scan_workspace
from .tags import build_dashboard_stats, default_tag_file, default_valid_tag_file


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Terminal dashboard for competitive-programming progress.")
    parser.add_argument("command", nargs="?", choices=("scan", "missing-tags"), help="Run a non-UI command.")
    parser.add_argument("--workspace", type=Path, default=default_workspace(), help="Competitive-programming workspace root.")
    parser.add_argument("--tags", type=Path, default=default_tag_file(), help="Path to problem_tags.json.")
    parser.add_argument("--valid-tags", type=Path, default=default_valid_tag_file(), help="Path to valid_tags.json.")
    args = parser.parse_args(argv)

    if args.command == "scan":
        _print_scan(args.workspace, args.tags, args.valid_tags)
        return
    if args.command == "missing-tags":
        _print_missing_tags(args.workspace, args.tags, args.valid_tags)
        return

    CptopApp(args.workspace, args.tags, args.valid_tags).run()


def _print_scan(workspace: Path, tag_file: Path, valid_tag_file: Path) -> None:
    stats = build_dashboard_stats(scan_workspace(workspace), workspace.resolve(), tag_file, valid_tag_file)
    print(f"Workspace: {stats.workspace}")
    print(f"Solved: {stats.solved}/{stats.total} ({stats.percent:.0f}%)")
    print(f"Untagged solved: {len(stats.missing_tag_keys)}")
    for platform in stats.platform_stats:
        print(f"{platform.name}: {platform.solved}/{platform.total} ({platform.percent:.0f}%)")
    for warning in stats.warnings:
        print(f"warning: {warning}")


def _print_missing_tags(workspace: Path, tag_file: Path, valid_tag_file: Path) -> None:
    stats = build_dashboard_stats(scan_workspace(workspace), workspace.resolve(), tag_file, valid_tag_file)
    if not stats.missing_tag_keys:
        print("No solved problems are missing tags.")
        return
    for key in stats.missing_tag_keys:
        print(key)
