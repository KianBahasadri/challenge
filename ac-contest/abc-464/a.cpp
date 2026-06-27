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
  std::string s;
  std::cin >> s;
  int count_e = 0;
  for (char c: s) {
    count_e += c == 'E';
  }
  if (count_e > s.size() / 2) {
    std::cout << "East\n";
  } else {
    std::cout << "West\n";
  }
  return 0;
}
