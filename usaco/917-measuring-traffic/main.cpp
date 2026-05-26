#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "traffic";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  int n;
  std::cin >> n;
  struct Segment {
    std::string t;
    int l, u;
  };
  std::vector<Segment> seg(n);

  for (int i=0; i<n; i++) {
    std::cin >> seg[i].t >> seg[i].l  >> seg[i].u;
  }
  int l = -1;
  int u;
  for (int i=n-1; i>-1; i--) {
    if (l == -1) {
      if (seg[i].t != "none") {
        continue;
      }
      l = seg[i].l;
      u = seg[i].u;
    }
    if (seg[i].t == "none") {
      l = std::max(l, seg[i].l);
      u = std::min(u, seg[i].u);
    } else if (seg[i].t  == "on") {
      l -= seg[i].u;
      u -= seg[i].l;
      l = std::max(l, 0);
    } else {
      l += seg[i].l;
      u += seg[i].u;
    }
  }
  std::cout << l << ' ' << u << '\n';
  l = -1;
  for (int i=0; i<n; i++) {
    if (l == -1) {
      if (seg[i].t != "none") {
        continue;
      }
      l = seg[i].l;
      u = seg[i].u;
    }
    if (seg[i].t == "none") {
      l = std::max(l, seg[i].l);
      u = std::min(u, seg[i].u);
    } else if (seg[i].t  == "on") {
      l += seg[i].l;
      u += seg[i].u;
    } else {
      l -= seg[i].u;
      u -= seg[i].l;
      l = std::max(l, 0);
    }
  }
  std::cout << l << ' ' << u << '\n';
  return 0;
}
