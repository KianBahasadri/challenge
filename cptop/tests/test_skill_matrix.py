from cptop.models import TagStats
from cptop.skill_matrix import plain_width, render_skill_matrix


def _bar_width(line: str) -> int:
    return line.count("█")


def test_skill_matrix_scales_against_strongest_skill() -> None:
    matrix = render_skill_matrix(
        (
            TagStats("number-theory", solved=22, total=22),
            TagStats("arrays", solved=8, total=8),
        )
    )

    assert "22" in matrix
    assert "8" in matrix
    assert "/22" not in matrix
    assert "%" not in matrix


def test_skill_matrix_groups_related_tags() -> None:
    matrix = render_skill_matrix(
        (
            TagStats("number-theory", solved=10, total=10),
            TagStats("dfs", solved=4, total=4),
            TagStats("segment-tree", solved=3, total=3),
            TagStats("binary-search", solved=2, total=2),
            TagStats("simulation", solved=1, total=1),
        ),
        available_width=100,
        available_height=30,
    )

    assert "MATH" in matrix
    assert "GRAPHS" in matrix
    assert "DATA STRUCTURES" in matrix
    assert "TECHNIQUES" in matrix
    assert "IMPLEMENTATION" in matrix


def test_skill_matrix_keeps_tagged_unsolved_skills_visible() -> None:
    matrix = render_skill_matrix(
        (
            TagStats("number-theory", solved=10, total=10),
            TagStats("dijkstra", solved=0, total=2),
        )
    )

    assert "dijkstra" in matrix
    assert "0" in matrix


def test_skill_matrix_rows_fit_available_width() -> None:
    width = 90
    matrix = render_skill_matrix(
        (
            TagStats("number-theory", solved=22, total=22),
            TagStats("frequency-counting", solved=5, total=5),
            TagStats("modular-arithmetic", solved=3, total=3),
        ),
        available_width=width,
        available_height=30,
    )

    assert max(plain_width(line) for line in matrix.splitlines()) <= width


def test_skill_matrix_preserves_full_tag_names_when_they_fit() -> None:
    matrix = render_skill_matrix(
        (
            TagStats("number-theory", solved=22, total=22),
            TagStats("frequency-counting", solved=5, total=5),
        ),
        available_width=100,
        available_height=30,
    )

    assert "number-theory" in matrix
    assert "frequency-counting" in matrix
    assert "number-theo-" not in matrix
    assert "frequency-c-" not in matrix


def test_skill_matrix_uses_consistent_bar_width_across_sections() -> None:
    matrix = render_skill_matrix(
        (
            TagStats("number-theory", solved=10, total=10),
            TagStats("topological-sort", solved=1, total=1),
            TagStats("stack", solved=1, total=1),
            TagStats("sliding-window", solved=2, total=2),
            TagStats("frequency-counting", solved=5, total=5),
            TagStats("greedy", solved=1, total=1),
        ),
        available_width=100,
        available_height=30,
    )

    bar_widths = {_bar_width(line) for line in matrix.splitlines() if "█" in line}

    assert len(bar_widths) == 1


def test_skill_matrix_uses_two_columns_on_wide_screens() -> None:
    matrix = render_skill_matrix(
        (
            TagStats("number-theory", solved=10, total=10),
            TagStats("dfs", solved=4, total=4),
            TagStats("segment-tree", solved=3, total=3),
            TagStats("binary-search", solved=2, total=2),
            TagStats("simulation", solved=1, total=1),
        ),
        available_width=140,
        available_height=30,
    )

    assert any("MATH" in line and "GRAPHS" in line for line in matrix.splitlines())
    assert max(plain_width(line) for line in matrix.splitlines()) <= 140


def test_skill_matrix_uses_two_columns_on_standard_terminals() -> None:
    matrix = render_skill_matrix(
        (
            TagStats("number-theory", solved=10, total=10),
            TagStats("dfs", solved=4, total=4),
            TagStats("segment-tree", solved=3, total=3),
            TagStats("binary-search", solved=2, total=2),
            TagStats("simulation", solved=1, total=1),
        ),
        available_width=100,
        available_height=30,
    )

    assert any("MATH" in line and "GRAPHS" in line for line in matrix.splitlines())
    assert max(plain_width(line) for line in matrix.splitlines()) <= 100


def test_skill_matrix_trims_to_available_height() -> None:
    matrix = render_skill_matrix(
        (
            TagStats("number-theory", solved=10, total=10),
            TagStats("combinatorics", solved=9, total=9),
            TagStats("primes", solved=8, total=8),
            TagStats("dfs", solved=7, total=7),
            TagStats("bfs", solved=6, total=6),
            TagStats("segment-tree", solved=5, total=5),
            TagStats("fenwick-tree", solved=4, total=4),
            TagStats("binary-search", solved=3, total=3),
            TagStats("simulation", solved=2, total=2),
        ),
        available_width=80,
        available_height=6,
    )

    assert len(matrix.splitlines()) == 6
    assert "..." in matrix
