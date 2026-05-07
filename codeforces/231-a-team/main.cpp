#include <iostream>
#include <cstdio>
#include <string>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  // std::string problemname = "name";
  // freopen(problemname + ".in", "r", stdin); // file io
  // freopen(problemname + ".out", "w", stdout);
  int n;
  std::cin >> n;
  int count = 0;
  while (n--) {
    int a, b, c;
    std::cin >> a >> b >> c;
    count += a + b + c > 1;
  }
  std::cout << count << '\n';
  return 0;
}
