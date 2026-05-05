from __future__ import annotations

from collections import defaultdict

from rich.markup import escape

from .models import TagStats


_GROUPS = {
    "Math": {
        "combinatorics",
        "game-theory",
        "geometry",
        "modular-arithmetic",
        "number-theory",
        "primes",
        "probability",
    },
    "Graphs": {
        "bfs",
        "dfs",
        "dijkstra",
        "flows",
        "graphs",
        "lca",
        "shortest-paths",
        "topological-sort",
        "trees",
    },
    "Data Structures": {
        "data-structures",
        "dsu",
        "fenwick-tree",
        "heap",
        "ordered-set",
        "segment-tree",
        "sparse-table",
        "stack",
        "trie",
    },
    "Techniques": {
        "binary-search",
        "bitmasks",
        "divide-and-conquer",
        "dp",
        "hashing",
        "kmp",
        "knapsack",
        "meet-in-the-middle",
        "recursion",
        "sliding-window",
        "two-pointers",
    },
    "Implementation": {
        "arrays",
        "brute-force",
        "constructive",
        "difference-array",
        "frequency-counting",
        "interactive",
        "prefix-sums",
        "simulation",
        "sorting",
    },
}

_TAG_TO_GROUP = {tag: group for group, tags in _GROUPS.items() for tag in tags}
_GROUP_ORDER = ("Math", "Graphs", "Data Structures", "Techniques", "Implementation", "Other")
_TWO_COLUMN_MIN_WIDTH = 96


def render_skill_matrix(
    rows: tuple[TagStats, ...],
    available_width: int | None = None,
    available_height: int | None = None,
) -> str:
    visible_rows = tuple(row for row in rows if row.total > 0)
    if not rows:
        return "[dim]No tags yet. Add data/problem_tags.json to map solved problems to skills.[/dim]"
    if not visible_rows:
        return "[dim]No completed tagged problems yet.[/dim]"

    max_solved = max(row.solved for row in visible_rows)
    if max_solved == 0:
        return "[dim]No completed tagged problems yet.[/dim]"
    groups = _group_rows(visible_rows)
    width = max(1, available_width or 100)
    height = max(1, available_height or 24)
    column_width = _column_width(width)
    label_width = _label_width(visible_rows, column_width, max_solved)

    blocks = [
        _render_group(group, group_rows, max_solved, column_width, label_width)
        for group in _GROUP_ORDER
        if (group_rows := groups.get(group))
    ]
    if _use_two_columns(width, blocks):
        return _render_columns(blocks, width, height)
    return "\n".join(_trim_height(_flatten_blocks(blocks), height))


def plain_width(text: str) -> int:
    width = 0
    in_markup = False
    for char in text:
        if char == "[":
            in_markup = True
        elif char == "]" and in_markup:
            in_markup = False
        elif not in_markup:
            width += 1
    return width


def _group_rows(rows: tuple[TagStats, ...]) -> dict[str, tuple[TagStats, ...]]:
    grouped: dict[str, list[TagStats]] = defaultdict(list)
    for row in rows:
        grouped[_TAG_TO_GROUP.get(row.name, "Other")].append(row)
    return {
        group: tuple(sorted(group_rows, key=lambda row: (-row.solved, -row.total, row.name.lower())))
        for group, group_rows in grouped.items()
    }


def _render_group(
    group: str,
    rows: tuple[TagStats, ...],
    max_solved: int,
    width: int,
    label_width: int,
) -> list[str]:
    title = f"[#94a3b8]{escape(group.upper())}[/]"
    return [title, *(_skill_row(row, max_solved, width, label_width) for row in rows), ""]


def _skill_row(row: TagStats, max_solved: int, width: int, label_width: int) -> str:
    metric_width = len(str(max_solved))
    bar_width = max(8, width - label_width - metric_width - 3)
    filled = min(bar_width, round(row.solved / max_solved * bar_width))
    empty = bar_width - filled
    label = _fit(row.name, label_width)
    metric = f"{row.solved:>{metric_width}}"
    return (
        f"[#f8fafc]{escape(label):<{label_width}}[/] "
        f"[#22d3ee]{'█' * filled}[/]"
        f"[#111827]{'█' * empty}[/] "
        f"[#cbd5e1]{metric}[/]"
    )


def _fit(text: str, width: int) -> str:
    if len(text) <= width:
        return text
    if width <= 1:
        return text[:width]
    return text[: width - 1] + "-"


def _label_width(rows: tuple[TagStats, ...], width: int, max_solved: int) -> int:
    metric_width = len(str(max_solved))
    return min(max(len(row.name) for row in rows), max(1, width - metric_width - 11))


def _column_width(width: int) -> int:
    if width >= _TWO_COLUMN_MIN_WIDTH:
        return max(1, (width - 6) // 2)
    return width


def _use_two_columns(width: int, blocks: list[list[str]]) -> bool:
    return width >= _TWO_COLUMN_MIN_WIDTH and len(blocks) > 1


def _render_columns(blocks: list[list[str]], width: int, height: int) -> str:
    left_blocks, right_blocks = _balanced_columns(blocks)
    left = _trim_height(_flatten_blocks(left_blocks), height)
    right = _trim_height(_flatten_blocks(right_blocks), height)
    column_width = _column_width(width)
    gap = max(4, width - column_width * 2)
    line_count = max(len(left), len(right))
    lines = []
    for index in range(line_count):
        left_line = left[index] if index < len(left) else ""
        right_line = right[index] if index < len(right) else ""
        lines.append(f"{_pad_markup(left_line, column_width)}{' ' * gap}{right_line}")
    return "\n".join(lines)


def _balanced_columns(blocks: list[list[str]]) -> tuple[list[list[str]], list[list[str]]]:
    left: list[list[str]] = []
    right: list[list[str]] = []
    left_height = 0
    right_height = 0
    for block in blocks:
        if left_height <= right_height:
            left.append(block)
            left_height += len(block)
        else:
            right.append(block)
            right_height += len(block)
    return left, right


def _flatten_blocks(blocks: list[list[str]]) -> list[str]:
    lines = [line for block in blocks for line in block]
    while lines and lines[-1] == "":
        lines.pop()
    return lines


def _trim_height(lines: list[str], height: int) -> list[str]:
    if len(lines) <= height:
        return lines
    if height <= 1:
        return lines[:height]
    return [*lines[: height - 1], "[dim]...[/dim]"]


def _pad_markup(text: str, width: int) -> str:
    return f"{text}{' ' * max(width - plain_width(text), 0)}"
