#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <array>
#include <utility>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "promote";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  
  std::string out;
  std::array<std::array<int, 2>, 4> p;
  for (int i =0; i<4; i++) {
    std::cin >> p[i][0] >> p[i][1];
  }
  int carry = 0;
  for (int i=3; i>0; i--) {
    out = std::to_string(p[i][1] + carry - p[i][0]) + "\n" + out;
    carry = p[i][1] + carry - p[i][0];
  }
  std::cout << out;
  return 0;
}
