---
redo: yes # yes | no
rating: 4/10 # /10
review-date: 2026-05-23 # YYYY-MM-DD
completed: no # yes | no
---
## Problem
Paste the statement/link here.
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
  // std::string problemname = "name";
  // freopen((problemname + ".in").c_str(), "r", stdin); // file io
  // freopen((problemname + ".out").c_str(), "w", stdout);
  int n, q;
  std::cin >> n >> q;
  std::vector<int> blocks(n, 0);
  std::vector<int> count(3*100000+1, 0);
  int removed = 0;
  count[0] = n;
  while (q--) {
    int t, x;
    std::cin >> t >> x;
    if (t == 1) {
      x -= 1;
      count[blocks[x]] -= 1;
      blocks[x] += 1;
      count[blocks[x]] += 1;
      if (count[removed] == 0) {
        removed += 1;
      }
    } else {
      int sum = 0;
      for (int i=x+removed; i < count.size(); i++) {
        sum += count[i];
      }
      std::cout << sum << '\n';
    }
  }
  return 0;  
}
```
## Editorial
Let us perform a simulation to process the queries. What we need to manage is:

- `A_i`, the number of blocks stacked on cell `i`.
- `B_j`, the number of cells with `j` or more blocks.

However, naively maintaining all entries of `B_j` every time a block is removed from all cells costs `Theta(Q^2)` in the worst case.

One improvement is to skip actually removing a block from every cell. In that non-removing simulation, for a type-2 query the answer is:

Let `k` be the minimum number of blocks stacked in any cell. Then print the number of cells with at least `y + k` blocks, namely `B_{y+k}`.

Finding the minimum `A_i` every query would cost `O(NQ)`, but `k` can be rephrased as the maximum `j` such that `B_j = N`. This value only changes during type-1 queries, and each update either increases it by one or leaves it unchanged, so it can be maintained in total `O(Q)` time.

Maintain `A`, `B`, and `k`:

- Initially, all `A_i = 0`, all `B_j = 0`, and `k = 0`.
- Type 1: increase `A_x`, increase `B_{A_x}`, and if `B_{A_x} = N`, set `k = A_x`.
- Type 2: print `0` if `k + y > Q`; otherwise print `B_{k+y}`.

Total complexity: `O(N+Q)`.
## Other People's Accepted Solutions
```cpp
#include <bits/stdc++.h>
using namespace std;
#define N (int)3e+5
int main(void){
	int a[N+1]={};
	int c[N+1]={};
	int n,q,t,x,mn=0;
	cin>>n>>q;
	for(int i=0;i<q;i++){
		cin>>t>>x;
		if(t==1){
			a[x]++;
			c[a[x]]++;
			if(c[a[x]]==n)mn=a[x];
		}
		if(t==2){
			if(x+mn>q)cout<<0<<endl;
			else cout<<c[x+mn]<<endl;
		}
	}
	return 0;
}
```
# AI Review
model: gpt-5
## My Approach
Maintain `blocks[i]` as the current unremoved height of each cell and `count[h]` as the number of cells currently at exact height `h`. `removed` is used as the lazy global removal offset: when every cell has moved past the current `removed` height, increment it. For type 1, update one cell's exact-height bucket. For type 2, sum all exact-height buckets from `x + removed` upward.
## Complexity
Time: `O(Q * max_height)` worst case, because each type-2 query may scan almost the whole `count` array.
Memory: `O(N+Q)`.
## Judgment
The bottleneck is the suffix sum in type 2:

```cpp
for (int i=x+removed; i < count.size(); i++) {
  sum += count[i];
}
```

With many type-2 queries, this can be about `3e5 * 3e5` operations. The needed value has to be available in `O(1)`, as in the editorial's `B_{k+y}`.
## Could This Be Simpler?
Yes: keep `count[h]` as the number of cells with at least `h` blocks, not exactly `h` blocks. Then type 2 is just one array lookup.
## Missed Observations
When a type-1 query increases one cell from `a` to `a+1`, exactly one new threshold becomes satisfied: `B_{a+1}` increases by 1. That avoids needing any suffix sum later.
## Editorial Comparison
The code has the same lazy-removal idea as the editorial with `removed` corresponding to `k`. The difference is the maintained array: the code stores exact-height counts, while the editorial stores at-least-height counts. That one difference changes type 2 from `O(Q)` to `O(1)`.
## Other Solution Comparison
The accepted solution increments `c[a[x]]` after each type-1 update and directly prints `c[x+mn]`. There is no loop in type 2.
## Key Lesson
If queries ask "at least y", try to maintain threshold counts directly instead of exact counts plus a suffix scan.
## Implementation
The array only needs size `q + 1`, since no height above the number of queries can matter.
# Redo Decision
Decision: yes
## Reason
The main idea was close, but the type-2 suffix loop misses the performance requirement.
## Focus If Redoing
Maintain "number of cells with at least this many blocks" and make type 2 a single lookup.
