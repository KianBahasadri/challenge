from __future__ import annotations

from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import DataTable, Footer, Label, Static

from .models import DashboardStats, PlatformStats, Problem, TagStats
from .scanner import scan_workspace
from .tags import build_dashboard_stats, default_tag_file


class CptopApp(App[None]):
    CSS = """
    Screen {
        background: #000000;
        color: #c8c8c8;
    }

    Footer {
        background: #000000;
        color: #9ca3af;
    }

    #topbar {
        height: 1;
        width: 100%;
        padding: 0 1;
        background: #000000;
        color: #eeeeee;
        text-style: bold;
        text-align: center;
    }

    #main {
        height: 1fr;
        padding: 1;
    }

    .page {
        height: 1fr;
        border: round #7aa27a;
        padding: 1 2;
        background: #000000;
    }

    .title {
        color: #eeeeee;
        text-style: bold;
        margin-bottom: 1;
        width: 100%;
        text-align: center;
    }

    .metric {
        color: #f8fafc;
    }

    .muted {
        color: #7b7f87;
    }

    #platform-bars {
        height: 1fr;
        color: #c8c8c8;
        content-align: center middle;
    }

    #platforms-summary {
        width: 100%;
        text-align: center;
    }

    DataTable {
        height: 1fr;
        background: #000000;
        border: none;
    }
    """

    BINDINGS = [
        ("left", "previous_page", "Previous"),
        ("right", "next_page", "Next"),
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]
    PAGES = ("platforms-page", "tags-page", "unsolved-page")

    def __init__(self, workspace: Path, tag_file: Path | None = None) -> None:
        super().__init__()
        self.workspace = workspace.resolve()
        self.tag_file = tag_file or default_tag_file()
        self.stats: DashboardStats | None = None
        self.page_index = 0

    def compose(self) -> ComposeResult:
        yield Static("", id="topbar")
        with Vertical(id="main"):
            with Vertical(classes="page", id="platforms-page"):
                yield Static(id="platforms-summary")
                yield Static(id="platform-bars")
            with Vertical(classes="page", id="tags-page"):
                yield Static(id="tags-summary")
                yield DataTable(id="tags")
            with Vertical(classes="page", id="unsolved-page"):
                yield Static(id="unsolved-summary")
                yield DataTable(id="unsolved")
        yield Footer()

    def on_mount(self) -> None:
        self.title = "cptop"
        self.sub_title = "competitive programming dashboard"
        self._configure_tables()
        self.refresh_stats()
        self._show_page()

    def action_refresh(self) -> None:
        self.refresh_stats()

    def action_next_page(self) -> None:
        self.page_index = (self.page_index + 1) % len(self.PAGES)
        self._show_page()

    def action_previous_page(self) -> None:
        self.page_index = (self.page_index - 1) % len(self.PAGES)
        self._show_page()

    def refresh_stats(self) -> None:
        problems = scan_workspace(self.workspace)
        self.stats = build_dashboard_stats(problems, self.workspace, self.tag_file)
        self._render_summaries(self.stats)
        self._render_platforms(self.stats.platform_stats)
        self._render_tags(self.stats.tag_stats)
        self._render_unsolved(tuple(problem for problem in self.stats.problems if not problem.solved))

    def _configure_tables(self) -> None:
        tags = self.query_one("#tags", DataTable)
        tags.cursor_type = "row"
        tags.add_columns("Tag", "Solved", "Total", "%", "Read")

        unsolved = self.query_one("#unsolved", DataTable)
        unsolved.cursor_type = "row"
        unsolved.add_columns("Platform", "Problem", "Link")

    def _show_page(self) -> None:
        for index, page_id in enumerate(self.PAGES):
            self.query_one(f"#{page_id}").display = index == self.page_index
        if self.stats:
            self._render_topbar(self.stats)

    def _render_topbar(self, stats: DashboardStats) -> None:
        page = self.page_index + 1
        labels = ("platform", "skills", "unsolved")
        nav = " ".join(
            f"[b]{index + 1}[/b] {label}" if index == self.page_index else f"[dim]{index + 1} {label}[/dim]"
            for index, label in enumerate(labels)
        )
        self.query_one("#topbar", Static).update(
            f"[red]{page}[/red] cptop  {nav}  "
            f"[green]{stats.solved}[/green]/{stats.total} solved  "
            f"[yellow]{stats.unsolved}[/yellow] unsolved"
        )

    def _render_summaries(self, stats: DashboardStats) -> None:
        best = max(stats.platform_stats, key=lambda item: item.percent, default=None)
        best_line = f"Best platform: {best.name} ({best.percent:.0f}%)" if best else "Best platform: n/a"
        weakest = next((tag for tag in stats.tag_stats if tag.total >= 2 and tag.percent < 60), None)
        strongest = max(stats.tag_stats, key=lambda item: (item.percent, item.total), default=None)
        skill_line = _skill_summary(strongest, weakest)

        self.query_one("#platforms-summary", Static).update(
            f"[b]Total:[/b] {stats.solved}/{stats.total} ({stats.percent:.0f}%)   "
            f"[b]Unsolved:[/b] {stats.unsolved}   {best_line}"
        )
        self.query_one("#tags-summary", Static).update(
            f"Tagged solved [b]{stats.solved - len(stats.missing_tag_keys)}[/b]/{stats.solved} | {skill_line}"
        )
        self.query_one("#unsolved-summary", Static).update(
            f"Unsolved [b]{stats.unsolved}[/b] problems across {sum(1 for row in stats.platform_stats if row.unsolved)} platforms"
        )
        self._render_topbar(stats)

    def _render_platforms(self, rows: tuple[PlatformStats, ...]) -> None:
        chart = self.query_one("#platform-bars", Static)
        if not rows:
            chart.update("[dim]No platforms found.[/dim]")
            return
        chart.update(_vertical_platform_bars(rows))

    def _render_tags(self, rows: tuple[TagStats, ...]) -> None:
        table = self.query_one("#tags", DataTable)
        table.clear()
        if not rows:
            table.add_row("No tags yet", "0", "0", "0%", "Add data/problem_tags.json")
            return
        for row in rows:
            table.add_row(row.name, str(row.solved), str(row.total), f"{row.percent:.0f}%", _read(row.percent))

    def _render_unsolved(self, rows: tuple[Problem, ...]) -> None:
        table = self.query_one("#unsolved", DataTable)
        table.clear()
        if not rows:
            table.add_row("All clear", "No unsolved problems", "")
            return
        for row in sorted(rows, key=lambda problem: (problem.platform.lower(), problem.name.lower())):
            table.add_row(row.platform, row.name, row.link or "")


def _vertical_platform_bars(rows: tuple[PlatformStats, ...]) -> str:
    height = 12
    cell_width = max(14, max(len(row.name) for row in rows) + 2)
    colors = tuple(_platform_color(index, row.name) for index, row in enumerate(rows))
    lines: list[str] = []

    for level in range(height, 0, -1):
        cells = []
        for index, row in enumerate(rows):
            filled_height = round(row.percent / 100 * height)
            color = colors[index]
            block = f"[{color}]██[/]" if filled_height >= level else "[#303030]██[/]"
            cells.append(_center_markup(block, 2, cell_width))
        lines.append("".join(cells))

    lines.append("".join(_center_markup(f"[{colors[index]}]{row.percent:.0f}%[/]", len(f"{row.percent:.0f}%"), cell_width) for index, row in enumerate(rows)))
    lines.append("".join(_center_text(f"{row.solved}/{row.total}", cell_width) for row in rows))
    lines.append("".join(_center_markup(f"[dim]{row.name}[/dim]", len(row.name), cell_width) for row in rows))
    return "\n".join(lines)


def _platform_color(index: int, name: str) -> str:
    platform_colors = {
        "codewars": "#f05656",
        "project_euler": "#ff8833",
        "dmoj": "#ffdd00",
        "codechef": "#713917",
        "hackerrank": "#2fc362",
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


def _read(percent: float) -> str:
    if percent >= 80:
        return "Strong"
    if percent >= 50:
        return "Stable"
    return "Train"


def _skill_summary(strongest: TagStats | None, weakest: TagStats | None) -> str:
    strong = f"Strongest: {strongest.name}" if strongest else "Strongest: n/a"
    weak = f"Train: {weakest.name}" if weakest else "Train: n/a"
    return f"{strong} | {weak}"
