import json
from pathlib import Path

from cptop.scanner import scan_workspace
from cptop.tags import build_dashboard_stats


def write_problem(root: Path, platform: str, name: str, solved: bool) -> None:
    problem = root / platform / name
    problem.mkdir(parents=True)
    (problem / "link.txt").write_text("https://example.com/problem", encoding="utf-8")
    if solved:
        (problem / "completed").write_text("", encoding="utf-8")


def test_dashboard_stats_groups_platforms_and_tags(tmp_path: Path) -> None:
    write_problem(tmp_path, "alpha", "a", True)
    write_problem(tmp_path, "alpha", "b", False)
    write_problem(tmp_path, "beta", "c", True)
    write_problem(tmp_path, "beta", "d", True)
    tag_file = tmp_path / "tags.json"
    tag_file.write_text(
        json.dumps(
            {
                "alpha/a": {"tags": ["arrays", "greedy", "not-real"]},
                "alpha/b": {"tags": ["arrays"]},
                "beta/d": {"tags": ["greedy"]},
            }
        ),
        encoding="utf-8",
    )

    stats = build_dashboard_stats(scan_workspace(tmp_path), tmp_path, tag_file)

    assert stats.solved == 3
    assert stats.total == 4
    assert stats.missing_tag_keys == ("beta/c",)
    assert [(platform.name, platform.solved) for platform in stats.platform_stats] == [("beta", 2), ("alpha", 1)]
    assert {tag.name: (tag.solved, tag.total) for tag in stats.tag_stats} == {
        "arrays": (1, 2),
        "greedy": (2, 2),
    }
    assert "not-real" not in {tag.name for tag in stats.tag_stats}
    assert any("Skipping unknown tag for alpha/a: not-real" == warning for warning in stats.warnings)
