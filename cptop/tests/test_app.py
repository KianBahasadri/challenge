from pathlib import Path

from cptop.app import CptopApp
from cptop.models import Problem
from textual.widgets import DataTable


def write_problem(root: Path, platform: str, name: str, solved: bool) -> None:
    problem = root / platform / name
    problem.mkdir(parents=True)
    (problem / "link.txt").write_text("https://example.com/problem", encoding="utf-8")
    if solved:
        (problem / "completed").write_text("", encoding="utf-8")


async def test_app_smoke_renders_dashboard(tmp_path: Path) -> None:
    write_problem(tmp_path, "cses", "intro", True)
    write_problem(tmp_path, "cses", "todo", False)
    tag_file = tmp_path / "tags.json"
    tag_file.write_text("{}", encoding="utf-8")

    app = CptopApp(tmp_path, tag_file)
    async with app.run_test() as pilot:
        await pilot.pause()
        assert app.query_one("#topbar")
        assert app.query_one("#platform-bars")
        assert app.query_one("#platforms-page").display is True

        await pilot.press("right")
        assert app.query_one("#skills-page").display is True
        assert app.query_one("#skills-matrix")

        await pilot.press("right")
        assert app.query_one("#unsolved-page").display is True
        assert app.query_one("#unsolved")


async def test_unsolved_table_shows_started_on(tmp_path: Path) -> None:
    write_problem(tmp_path, "cses", "todo", False)
    tag_file = tmp_path / "tags.json"
    tag_file.write_text("{}", encoding="utf-8")

    app = CptopApp(tmp_path, tag_file)
    async with app.run_test() as pilot:
        await pilot.press("right", "right")
        table = app.query_one("#unsolved", DataTable)
        row = table.get_row_at(0)

    assert row[0]
    assert " " in str(row[0])
    assert row[1] == "cses"
    assert row[2] == "todo"
    assert row[3] == "https://example.com/problem"


async def test_unsolved_table_orders_oldest_to_newest(tmp_path: Path) -> None:
    tag_file = tmp_path / "tags.json"
    tag_file.write_text("{}", encoding="utf-8")

    app = CptopApp(tmp_path, tag_file)
    async with app.run_test() as pilot:
        await pilot.press("right", "right")
        app._render_unsolved(
            (
                Problem("cses", "newer", tmp_path / "newer", False, started_on="Jan 2", started_at=2),
                Problem("cses", "older", tmp_path / "older", False, started_on="Jan 1", started_at=1),
            )
        )
        table = app.query_one("#unsolved", DataTable)
        names = [table.get_row_at(index)[2] for index in range(table.row_count)]

    assert names == ["older", "newer"]


async def test_enter_opens_selected_unsolved_problem(tmp_path: Path, monkeypatch) -> None:
    write_problem(tmp_path, "cses", "intro", True)
    write_problem(tmp_path, "cses", "todo", False)
    tag_file = tmp_path / "tags.json"
    tag_file.write_text("{}", encoding="utf-8")
    opened: list[list[str]] = []

    def fake_popen(args, **kwargs):
        opened.append(args)

    monkeypatch.setattr("cptop.app.subprocess.Popen", fake_popen)

    app = CptopApp(tmp_path, tag_file)
    async with app.run_test() as pilot:
        await pilot.press("right", "right", "enter")
        await pilot.pause()

    assert opened == [["firefox", "https://example.com/problem"]]
