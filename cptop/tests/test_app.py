from pathlib import Path

from cptop.app import CptopApp


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
        assert app.query_one("#tags-page").display is True

        await pilot.press("right")
        assert app.query_one("#unsolved-page").display is True
        assert app.query_one("#unsolved")
