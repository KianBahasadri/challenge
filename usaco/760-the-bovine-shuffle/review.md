---
redo: yes # yes | no
rating: 6 # /10
review-date: 2026-05-12 # YYYY-MM-DD
---
## Problem
http://www.usaco.org/index.php?page=viewproblem2&cpid=760
## My Accepted Code
```cpp
#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "shuffle";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);

  int n;
  std::cin >> n;
  std::vector<int> a(n);
  std::vector<int> b(n);
  std::vector<int> cows(n);
  std::vector<int> next(n);
  for (int i=0; i<n;i++) {
    std::cin >> a[i];
  }
  for (int i=0; i<n;i++) {
    std::cin >> cows[i];
  }

  for (int i=0; i<n;i++) {
    for (int j=0; j<n;j++) {
      if (a[j] == i+1) {
        b[i] = j+1;
        break;
      }
    }
  }
        
  for (int j=0; j<3;j++) {
    for (int i=0; i<n;i++) {
      next[b[i]-1] = cows[i];
    }
    cows = next;
  }

  for (int i=0; i<n;i++) {
    std::cout << cows[i] << '\n';
  }
  return 0;
}
```
## Editorial
Optional. Paste the editorial or link here.

If the cow in position ii moves to position aiai​ after one shuffle, then after that shuffle the cow sitting at aiai​ must have come from ii.

To undo a single shuffle, for each current position jj we find the unique ii satisfying ai=jai​=j and move the cow at jj back to ii. Repeating this step three times recovers the original ordering before any shuffles.

## Other People's Accepted Solutions
Optional. Paste alternate accepted solutions or links here.
Separate multiple solutions with a line containing only `---`.

#include <bits/stdc++.h>
using namespace std;

const int SHUFFLE_NUM = 3;

int main() {
	freopen("shuffle.in", "r", stdin);
	int n;
	cin >> n;

	vector<int> shuffle(n);
	for (int &i : shuffle) { cin >> i; }
	vector<int> ids(n);
	for (int &i : ids) { cin >> i; }

	for (int i = 0; i < SHUFFLE_NUM; i++) {
		vector<int> past_order(n);
		for (int j = 0; j < n; j++) {
			// -1 because the shuffle input starts from 1
			past_order[j] = ids[shuffle[j] - 1];
		}
		ids = past_order;
	}

	freopen("shuffle.out", "w", stdout);
	for (const int &i : ids) { cout << i << '\n'; }
}

# AI Review
model: GPT-5
## My Approach
Read the shuffle permutation `a` and the final cow ordering.

The code first builds `b`, where `b[i]` is the original position that maps into final position `i + 1`. It does this by scanning through `a` for each possible target position.

Then it applies that reverse mapping three times:

```cpp
next[b[i]-1] = cows[i];
```

After three reverse shuffles, `cows` contains the original ordering and gets printed.
## Complexity
Time: O(n^2)

Memory: O(n)
## Judgment
The only real cost issue is building `b` with a nested loop. Since `a` is a permutation, the inverse can be built in O(n), or avoided entirely for this problem.
## Could This Be Simpler?
Yes. The shuffle array can be used directly while undoing each shuffle:

```cpp
next[i] = cows[a[i] - 1];
```

That removes `b` and the O(n^2) inverse-building loop.
## Missed Observations
`a[i]` already tells which current position contains the cow that used to be at position `i`, so reversing one shuffle does not require searching for every value.
## Editorial Comparison
Matches the editorial idea of undoing the shuffle three times, but uses an extra inverse permutation step.
## Other Solution Comparison
The other accepted solution avoids constructing `b` and does each reverse shuffle directly in O(n), so its total time is O(n).
## Key Lesson
For permutation problems, check whether you need the inverse permutation or whether the given direction already lets you pull values into their previous positions.
## Implementation
`cows = next;` copies all `n` values each pass. `cows.swap(next);` avoids the copy, as long as every element of `next` is overwritten before the next swap.
# Redo Decision
Decision: yes
## Reason
Redo once to practice using the permutation directly and getting the solution down to O(n) with fewer moving parts.
## Focus If Redoing
Use one temporary vector and write the reverse transition directly from `a`.
