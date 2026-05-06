# coach

`coach` is a CLI for this competitive-programming workspace.

It has two jobs:

- observe the current workspace state from existing problem directories and solved markers
- start a local terminal LLM (`opencode` or `codex`) coaching session without calling external APIs directly

## Run

```bash
./coach summary
./coach list --unsolved --limit 20
./coach recent --limit 10
./coach chat
```

By default, `coach` treats the parent of this directory as the CP workspace. Override it with:

```bash
./coach --workspace /path/to/challenge summary
```

## Commands

```bash
./coach summary
```

Prints total solved/unsolved counts and per-platform counts.

```bash
./coach list --solved
./coach list --unsolved
./coach list --platform cses --limit 10
```

Lists problems detected from `link.txt` files.

```bash
./coach recent
```

Shows recently started problem directories.

```bash
./coach chat
./coach chat --agent codex
./coach chat --agent opencode "Help me think through my current problem."
```

Starts an interactive local LLM session with the same workspace snapshot. Use `--dry-run` to inspect the command and opening prompt without starting the chat.

## Tests

The CLI itself only uses the Python standard library. Tests use `pytest` if it is already installed:

```bash
PYTHONPATH=src python3 -m pytest tests
```
