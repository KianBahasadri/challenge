from __future__ import annotations

from .models import PlatformStats


def render_platform_bars(rows: tuple[PlatformStats, ...]) -> str:
    height = 12
    cell_width = max(14, max(len(row.name) for row in rows) + 2)
    colors = tuple(platform_color(index, row.name) for index, row in enumerate(rows))
    lines: list[str] = []

    for level in range(height, 0, -1):
        cells = []
        for index, row in enumerate(rows):
            filled_height = round(row.percent / 100 * height)
            color = colors[index]
            block = f"[{color}]██[/]" if filled_height >= level else "[#303030]██[/]"
            cells.append(_center_markup(block, 2, cell_width))
        lines.append("".join(cells))

    lines.append(
        "".join(
            _center_markup(f"[{colors[index]}]{row.percent:.0f}%[/]", len(f"{row.percent:.0f}%"), cell_width)
            for index, row in enumerate(rows)
        )
    )
    lines.append("".join(_center_text(f"{row.solved}/{row.total}", cell_width) for row in rows))
    lines.append("".join(_center_markup(f"[dim]{row.name}[/dim]", len(row.name), cell_width) for row in rows))
    return "\n".join(lines)


def platform_color(index: int, name: str) -> str:
    platform_colors = {
        "codewars": "#f05656",
        "project_euler": "#ff8833",
        "dmoj": "#ffdd00",
        "codechef": "#713917",
        "hackerrank": "#2fc362",
        "usaco": "#075195",
    }
    if name in platform_colors:
        return platform_colors[name]
    colors = ("green", "cyan", "magenta", "yellow", "red", "blue")
    return colors[index % len(colors)]


def _center_text(text: str, width: int) -> str:
    return f"{text:^{width}}"


def _center_markup(markup: str, visible_width: int, width: int) -> str:
    left = max((width - visible_width) // 2, 0)
    right = max(width - visible_width - left, 0)
    return f"{' ' * left}{markup}{' ' * right}"
