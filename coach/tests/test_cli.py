from pathlib import Path

from coach.cli import print_summary
from coach.models import PlatformStats, Problem, WorkspaceStats


def test_print_summary_aligns_platform_columns(capsys, tmp_path: Path) -> None:
    stats = WorkspaceStats(
        workspace=tmp_path,
        problems=(
            Problem(platform="cses", name="one", path=tmp_path / "cses" / "one", solved=True),
            Problem(platform="long_platform", name="two", path=tmp_path / "long_platform" / "two", solved=False),
        ),
        platforms=(
            PlatformStats(name="long_platform", solved=12, total=100),
            PlatformStats(name="cses", solved=1, total=2),
        ),
    )

    print_summary(stats)

    assert capsys.readouterr().out.splitlines() == [
        f"Workspace: {tmp_path}",
        "Solved:    1/2 (50%)",
        "Unsolved:  1",
        "long_platform  12/100  (12%)",
        "cses            1/  2  (50%)",
    ]
