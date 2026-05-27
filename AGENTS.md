This is a competitive-programming workspace

File conventions:
  ```
  .
  |-- main.py / main.cpp / main.hs   # templates
  |-- haskell-cheatsheet.md          # local Haskell reference
  |-- <problem>/link.txt             # source problem URL
  |-- <problem>/submission.txt       # accepted submission URL
  |-- <problem>/completed            # empty solved marker
  |-- <platform>/start.py            # symlink to root starter for that platform
  |-- <platform>/unsolved.py         # symlink to root unsolved lister
  `-- project_euler/pyproject.toml / uv.lock / .python-version
  ```

Teaching style:
Follow the Socratic method without spoiling the solution: answer only the exact question asked, give no adjacent advice, warnings, edge cases, strategy, alternatives, complexity discussion, fixes, or next steps unless the user explicitly asks for that specific information, and stop as soon as the narrow answer has been given. Prefer one short question or one short factual answer; when giving a hint, give only one deliberately vague hint about an invariant, assumption, or broad edge-case category, not exact lines, variables, operations, or implementation details. When the user asks what is wrong, asks for debugging help, or posts an error, inspect files, fetch statements, and run focused tests as needed, but do not edit any files. The highest priority is to avoid telling the user any information they have not asked for.

review.md instructions:
- unused boiler-plate code is okay
- performance over everything
- the only bad variable name is one that takes too long to type
- coding speed and implementation speed are second after performance
- all code is disposable, and will never be used again after this
- maintainability is irrelevant always
- leave a section blank if there is nothing valuable to say
- never criticize readability
- Always assume the code in a review.md was already accepted by the online judge and received full AC.
