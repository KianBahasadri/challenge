#include <iostream>
#include <cstdio>
#include <string>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "teleport";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  int a, b, x, y;
  std::cin >> a >> b >> x >> y;
  int ab = std::abs(a - b);
  int xy = std::abs(a - x) + std::abs( y - b);
  int yx = std::abs(a - y) + std::abs( x - b);
  std::cout << std::min(ab, std::min(xy, yx));
  return 0;  
}
