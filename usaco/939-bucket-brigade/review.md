---
redo: no # yes | no
rating: 8 # /10
review-date: 2026-05-09 # YYYY-MM-DD
---
## Problem
https://usaco.org/index.php?page=viewproblem2&cpid=939
## My Accepted Code
```cpp
#include <iostream>
#include <cstdio>
#include <string>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "buckets";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  int bx, by, rx, ry, lx, ly;
  for (int x = 0; x < 10; x++) {
    for (int y=0; y<10; y++) {
      char c;
      std::cin >> c;
      if (c == 'B') {
        bx = x;
        by = y;
      } else if (c == 'R') {
        rx = x;
        ry = y;
      } else if (c == 'L') {
        lx = x;
        ly = y;
      }
    }
  }
  int diff = std::abs(bx - lx) + std::abs(by - ly) - 1;
  bool btwn_x = (bx < rx && rx < lx) || (lx < rx && rx < bx);
  bool btwn_y = (by < ry && ry < ly) || (ly < ry && ry < by);
  if (bx == rx && rx == lx && btwn_y) {
    diff += 2;
  } else if (by == ry && ry == ly && btwn_x) {
    diff += 2;
  }
  std::cout << diff << '\n';
  return 0;
}
```
## Editorial
Optional. Paste the editorial or link here.
## Other People's Accepted Solutions
Optional. Paste alternate accepted solutions or links here.
Separate multiple solutions with a line containing only `---`.
# AI Review
model: GPT-5
## My Approach
Scan the 10x10 grid and store the coordinates of `B`, `R`, and `L`.

The baseline answer is the Manhattan distance from `B` to `L`, minus 1, because the count is the number of empty cells between them along a shortest path:

```cpp
abs(bx - lx) + abs(by - ly) - 1
```

The only obstruction case is when all three objects are on the same row or the same column and `R` is strictly between `B` and `L`. In that case every shortest straight route is blocked, so the cow must detour around the rock, adding 2 extra moves.
## Complexity
Time: O(100)

Memory: O(1)
## Judgment

## Could This Be Simpler?

## Missed Observations

## Editorial Comparison
Matches the standard intended idea: Manhattan distance, with a `+2` correction only for the same-row or same-column blocked case.
## Other Solution Comparison

## Key Lesson
For grid geometry problems, first compute the unconstrained shortest path, then isolate the exact condition where an obstacle can force a detour. Here, the rock matters only when it is collinear with both endpoints and strictly between them.
## Implementation
`freopen("buckets.in", "r", stdin);` and `freopen("buckets.out", "w", stdout);` would be slightly faster to write than constructing `problemname + ".in"` / `".out"`.

The `isvowel` helper is unused. It does not matter for AC, but deleting template leftovers before submitting can make compile errors less likely if the helper depends on missing headers in a different problem.
# Redo Decision
Decision: no
## Reason
The accepted solution is already the intended O(1) approach and handles the only real edge case: the rock strictly between the barn and lake on the same row or column.
## Focus If Redoing
