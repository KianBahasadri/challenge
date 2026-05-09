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
