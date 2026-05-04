# cptop

`cptop` is a terminal dashboard for this competitive-programming workspace. It scans the parent workspace read-only, detects solved problems from existing markers, and combines that with curated tags stored inside this isolated directory.

## Run

```bash
uv run cptop
```

Useful non-UI commands:

```bash
uv run cptop scan
uv run cptop missing-tags
```

By default, `cptop` treats the parent of this directory as the CP workspace. You can override that:

```bash
uv run cptop --workspace /path/to/challenge
```

## Tags

Curated tags live in `data/problem_tags.json` and are keyed by `platform/problem`:

```json
{
  "cses/1068-weird-algorithm": {
    "tags": ["implementation", "simulation"],
    "difficulty": "easy",
    "notes": "Collatz sequence warmup."
  }
}
```

The dashboard will work without tags, but the strengths and weaknesses panels become more useful as solved problems are tagged.
