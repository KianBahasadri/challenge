---
redo: # yes | no
rating: # /10
review-date: 2026-05-28 # YYYY-MM-DD
completed: yes # yes | no
---
## Problem
https://usaco.org/index.php?page=viewproblem2&cpid=526
## My Accepted Code
```cpp
#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <list>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "censor";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  std::string s, t;
  std::cin >> s >> t;
  std::list<char> l(s.begin(), s.end());
  std::list<char>::iterator i = l.begin();
  while (i != l.end()) {
    bool found = true;
    std::list<char>::iterator ii = i;
    for (int j=0; j < t.size(); j++) {
      if (*ii != t[j]) {
        found = false;
        break;
      }
      ii++;
    }
    if (found) {
      i = l.erase(i, ii);
      int j = t.size();
      while (j-- && i != l.begin()) {
        i--;
      }
    } else {
      i++;
    }
  }
  std::string out(l.begin(), l.end());
  std::cout << out << '\n';
  return 0;
}
```
## Editorial
Explanation

Let us define censoredcensored as the final censored text.

We can iterate through every character of ss, appending it to censoredcensored. However, whenever we append a character we we need to check if censoredcensored ends with the censored word. If it does, we remove it from censoredcensored by taking off the last few characters.

As a demonstration, let's try this on the example case where:
s=whatthemomooofunt=moo
st​=whatthemomooofun=moo​

Our solution will loop through each character of ss, appending it to censoredcensored until it becomes whatthemomoowhatthemomoo, when it will cut off the last 3 characters since they equal tt. This results in censoredcensored becoming whatthemowhatthemo. Right after this, censoredcensored becomes whatthemoowhatthemoo as the next letter in ss is oo, so we omit the last 3 characters again and censoredcensored becomes whatthewhatthe.

After this, the check isn't triggered anymore, so we end up with whatthefunwhatthefun as our final word.
Implementation

Time Complexity: O(S⋅T)O(S⋅T)

#include "bits/stdc++.h"
using namespace std;

void setIO(string name = "") {
	cin.tie(0)->sync_with_stdio(0);
	if ((int)name.size()) {
		freopen((name + ".in").c_str(), "r", stdin);
		freopen((name + ".out").c_str(), "w", stdout);
	}
}

int main() {
	setIO("censor");
	string s;
	string t;
	cin >> s >> t;

	string censored;
	// Add each character to the censored string
	for (int i = 0; i < s.size(); i++) {
		censored += s[i];
		// If the end of the string is t, we remove t from the end
		if (censored.size() >= t.size() &&
		    censored.substr(censored.size() - t.size()) == t) {
			censored.resize(censored.size() - t.size());
		}
	}
	cout << censored << endl;
}

## Other People's Accepted Solutions
Optional. Paste alternate accepted solutions or links here.
Separate multiple solutions with a line containing only `---`.
# AI Review
model: GPT-5 Codex
## My Approach
The code stores the current string in a `std::list<char>` so removing a matched range does not shift later characters. It scans with iterator `i`, compares the next `t.size()` characters against `t`, erases the range if it matches, then backs up by up to `t.size()` positions so newly-adjacent characters can be reconsidered.
## Complexity
Time: O(|S| * |T|)
Memory: O(|S|)
## Judgment
The main cost is iterator walking through a linked list: each character comparison is pointer chasing, so the constant factor is much worse than a contiguous `std::string`/`vector<char>` stack approach.
## Could This Be Simpler?
Yes. Building an output string left-to-right and deleting from its end when the suffix equals `t` is shorter and faster in practice.
## Missed Observations
After processing a prefix of `s`, only the suffix of the constructed answer can become a new occurrence of `t`.
## Editorial Comparison
The editorial uses the same high-level invariant, but represents the current answer as a normal string and only checks/removes at the end. Your solution instead keeps the mutable text as a list and scans around erased regions.
## Other Solution Comparison

## Key Lesson
When deletions only matter at the end of a constructed answer, a stack-like string often beats a linked list even if linked-list erase is O(1).
## Implementation
`std::string` works well as a stack here: `push_back`, suffix comparison, and `resize` avoid list iterators and keep memory contiguous.
# Redo Decision
Decision: no
## Reason
The solution was accepted, and the important missed idea is already captured above.
## Focus If Redoing
