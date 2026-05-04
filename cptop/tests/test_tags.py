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
    tag_file = tmp_path / "tags.json"
    tag_file.write_text(
        json.dumps(
            {
                "alpha/a": {"tags": ["math", "greedy"]},
                "alpha/b": {"tags": ["math"]},
            }
        ),
        encoding="utf-8",
    )

    stats = build_dashboard_stats(scan_workspace(tmp_path), tmp_path, tag_file)

    assert stats.solved == 2
    assert stats.total == 3
    assert stats.missing_tag_keys == ("beta/c",)
    assert {platform.name: platform.solved for platform in stats.platform_stats} == {"alpha": 1, "beta": 1}
    assert {tag.name: (tag.solved, tag.total) for tag in stats.tag_stats} == {
        "math": (1, 2),
        "greedy": (1, 1),
    }
