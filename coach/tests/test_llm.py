from pathlib import Path

from coach.llm import build_coaching_prompt, interactive_command_for_agent
from coach.models import PlatformStats, Problem, WorkspaceStats


def test_build_coaching_prompt_includes_workspace_snapshot(tmp_path: Path) -> None:
    stats = WorkspaceStats(
        workspace=tmp_path,
        problems=(
            Problem(platform="cses", name="one", path=tmp_path / "cses" / "one", solved=True),
            Problem(platform="cses", name="two", path=tmp_path / "cses" / "two", solved=False),
        ),
        platforms=(PlatformStats(name="cses", solved=1, total=2),),
    )

    prompt = build_coaching_prompt(stats, "What next?", limit=5)

    assert "Progress: 1/2 solved" in prompt
    assert "- cses: 1/2 solved" in prompt
    assert "- cses/two" in prompt
    assert "What next?" in prompt


def test_interactive_command_for_agent_starts_chat_entrypoints(tmp_path: Path) -> None:
    assert interactive_command_for_agent("opencode", "help me", tmp_path) == [
        "opencode",
        str(tmp_path),
        "--prompt",
        "help me",
    ]
    assert interactive_command_for_agent("codex", "help me", tmp_path) == ["codex", "--cd", str(tmp_path), "help me"]
