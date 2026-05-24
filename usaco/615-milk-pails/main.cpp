#include <iostream>
#include <cstdio>
#include <string>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "pails";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  
  int x, y, m;
  std::cin >> x >> y >> m;
  int count[2] = {m/x, 0};
  int max = (m/x) * x;
  while (count[0] != 0) {
    count[0]--;
    if (count[0] * x + count[1] * y + y <= m) {
      count[1]++;
    }
    max = std::max(count[0] * x + count[1] * y, max);
  }
  std::cout << max << '\n';
  return 0;
}
