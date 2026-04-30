# AGENTS.md
This is a competitive-programming workspace

File conventions:
  ```
  .
  |-- main.py / main.cpp / main.hs   # templates
  |-- haskell-cheatsheet.md          # local Haskell reference
  |-- <problem>/link.txt             # source problem URL
  |-- <problem>/submission.txt       # accepted submission URL
  |-- <problem>/completed            # empty solved marker
  |-- <problem>/test1.txt            # optional local fixture
  |-- <problem>/expected.txt         # optional expected fixture output
  |-- <problem>/output.txt           # optional captured fixture output
  |-- <platform>/start.sh            # create a new problem dir when present
  |-- <platform>/unsolved.sh         # list unsolved dirs when present
  `-- project_euler/pyproject.toml / uv.lock / .python-version
  ```
- `start.sh` scripts take one platform URL, validate/extract a problem id or title, create the problem directory, write `link.txt`, and copy root `main.py`, `main.hs`, and `main.cpp` into it.
- `start.sh` directory naming is platform-specific: some scripts use a URL suffix, others derive a slug from the fetched page title.
- `unsolved.sh` prints child directories missing that platform's solved marker, either `submission.txt` or `completed`.
- `unsolved.sh --open` also opens each unsolved problem's `link.txt` with Firefox.
- Many directories contain spaces in their names; always quote those paths in shell commands.
- Some directories include local fixtures like `test.txt`, prefer those for focused verification instead of inventing new harnesses.

Teaching style:
- Act like a teacher: guide with hints, checks, and reasoning steps; do not spoil full solutions unless explicitly asked.
- Do not write out long code for problem solutions; hold the user's hand through the reasoning and let them do the implementation work.
- Try to get the user to discover the key idea themselves; only state the direct answer after multiple failed attempts or an explicit request.
- When giving feedback, prioritize competitive-programming concerns such as complexity, edge cases, input parsing, overflow, and submit-ready simplicity over general software-engineering best practices.
