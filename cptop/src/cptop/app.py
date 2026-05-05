from __future__ import annotations

import subprocess
from pathlib import Path

from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import DataTable, Footer, Static

from .models import DashboardStats, PlatformStats, Problem, TagStats
from .platform_chart import render_platform_bars
from .scanner import scan_workspace
from .skill_matrix import render_skill_matrix
from .tags import build_dashboard_stats, default_tag_file, default_valid_tag_file


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

    #skills-matrix {
        width: 1fr;
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
        ("enter", "open_selected_problem", "Open"),
        ("q", "quit", "Quit"),
        ("r", "refresh", "Refresh"),
    ]
    PAGES = ("platforms-page", "skills-page", "unsolved-page")

    def __init__(self, workspace: Path, tag_file: Path | None = None, valid_tag_file: Path | None = None) -> None:
        super().__init__()
        self.workspace = workspace.resolve()
        self.tag_file = tag_file or default_tag_file()
        self.valid_tag_file = valid_tag_file or default_valid_tag_file()
        self.stats: DashboardStats | None = None
        self.page_index = 0

    def compose(self) -> ComposeResult:
        yield Static("", id="topbar")
        with Vertical(id="main"):
            with Vertical(classes="page", id="platforms-page"):
                yield Static(id="platforms-summary")
                yield Static(id="platform-bars")
            with Vertical(classes="page", id="skills-page"):
                yield Static(id="skills-matrix")
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

    def action_open_selected_problem(self) -> None:
        if self.PAGES[self.page_index] != "unsolved-page":
            return
        table = self.query_one("#unsolved", DataTable)
        self._open_unsolved_row(table, table.cursor_row)

    def on_data_table_row_selected(self, event: DataTable.RowSelected) -> None:
        if event.data_table.id == "unsolved":
            self._open_unsolved_row(event.data_table, event.cursor_row)

    def _open_unsolved_row(self, table: DataTable, row_index: int) -> None:
        if not table.is_valid_row_index(row_index):
            return
        row = table.get_row_at(row_index)
        link = row[-1] if row else ""
        if not link:
            return
        subprocess.Popen(["firefox", str(link)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def on_resize(self) -> None:
        if self.stats:
            self._render_skills(self.stats.tag_stats)

    def refresh_stats(self) -> None:
        problems = scan_workspace(self.workspace)
        self.stats = build_dashboard_stats(problems, self.workspace, self.tag_file, self.valid_tag_file)
        self._render_summaries(self.stats)
        self._render_platforms(self.stats.platform_stats)
        self._render_skills(self.stats.tag_stats)
        self._render_unsolved(tuple(problem for problem in self.stats.problems if not problem.solved))

    def _configure_tables(self) -> None:
        unsolved = self.query_one("#unsolved", DataTable)
        unsolved.cursor_type = "row"
        unsolved.add_columns("Started on", "Platform", "Problem", "Link")

    def _show_page(self) -> None:
        for index, page_id in enumerate(self.PAGES):
            self.query_one(f"#{page_id}").display = index == self.page_index
        if self.PAGES[self.page_index] == "unsolved-page":
            self.query_one("#unsolved", DataTable).focus()
        if self.stats:
            self._render_topbar()

    def _render_topbar(self) -> None:
        labels = ("platform", "skills", "unsolved")
        nav = " ".join(
            f"[b]{label}[/b]" if index == self.page_index else f"[dim]{label}[/dim]"
            for index, label in enumerate(labels)
        )
        self.query_one("#topbar", Static).update(nav)

    def _render_summaries(self, stats: DashboardStats) -> None:
        self.query_one("#platforms-summary", Static).update(
            f"[b]Total:[/b] {stats.solved}/{stats.total} ({stats.percent:.0f}%)   "
            f"[b]Unsolved:[/b] {stats.unsolved}"
        )
        self.query_one("#unsolved-summary", Static).update(
            f"Unsolved [b]{stats.unsolved}[/b] problems across {sum(1 for row in stats.platform_stats if row.unsolved)} platforms"
        )
        self._render_topbar()

    def _render_platforms(self, rows: tuple[PlatformStats, ...]) -> None:
        chart = self.query_one("#platform-bars", Static)
        if not rows:
            chart.update("[dim]No platforms found.[/dim]")
            return
        chart.update(render_platform_bars(rows))

    def _render_skills(self, rows: tuple[TagStats, ...]) -> None:
        matrix = self.query_one("#skills-matrix", Static)
        matrix.update(render_skill_matrix(rows, matrix.size.width, matrix.size.height))

    def _render_unsolved(self, rows: tuple[Problem, ...]) -> None:
        table = self.query_one("#unsolved", DataTable)
        table.clear()
        if not rows:
            table.add_row("", "All clear", "No unsolved problems", "")
            return
        for row in sorted(
            rows,
            key=lambda problem: (
                problem.started_at is None,
                problem.started_at or 0,
                problem.platform.lower(),
                problem.name.lower(),
            ),
        ):
            table.add_row(row.started_on or "", row.platform, row.name, row.link or "")
