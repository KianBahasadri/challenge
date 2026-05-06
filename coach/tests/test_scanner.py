from pathlib import Path

from coach.scanner import build_stats, scan_workspace


def write_problem(root: Path, platform: str, name: str, solved_marker: str | None = None) -> None:
    problem = root / platform / name
    problem.mkdir(parents=True)
    (problem / "link.txt").write_text("https://example.com/problem", encoding="utf-8")
    if solved_marker:
        (problem / solved_marker).write_text("", encoding="utf-8")


def test_scan_workspace_detects_problem_dirs_and_solved_markers(tmp_path: Path) -> None:
    write_problem(tmp_path, "cses", "one", "submission.txt")
    write_problem(tmp_path, "cses", "two", None)
    write_problem(tmp_path, "project_euler", "1", "completed")
    (tmp_path / "main.py").write_text("", encoding="utf-8")

    problems = scan_workspace(tmp_path)

    assert [problem.key for problem in problems] == ["cses/one", "cses/two", "project_euler/1"]
    assert {problem.key: problem.solved for problem in problems} == {
        "cses/one": True,
        "cses/two": False,
        "project_euler/1": True,
    }


def test_scan_workspace_detects_nested_usaco_guide_problems(tmp_path: Path) -> None:
    problem = tmp_path / "usaco.guide" / "silver" / "prefix-sums" / "breed-counting"
    problem.mkdir(parents=True)
    (problem / "link.txt").write_text("https://example.com/usaco", encoding="utf-8")
    (problem / "submission.txt").write_text("", encoding="utf-8")

    problems = scan_workspace(tmp_path)

    assert [problem.key for problem in problems] == ["usaco/silver/prefix-sums/breed-counting"]
    assert problems[0].solved is True


def test_build_stats_summarizes_platforms(tmp_path: Path) -> None:
    write_problem(tmp_path, "cses", "one", "submission.txt")
    write_problem(tmp_path, "cses", "two", None)

    stats = build_stats(tmp_path)

    assert stats.solved == 1
    assert stats.total == 2
    assert stats.unsolved == 1
    assert [(platform.name, platform.solved, platform.total) for platform in stats.platforms] == [("cses", 1, 2)]
