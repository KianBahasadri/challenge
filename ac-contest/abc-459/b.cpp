#include <iostream>
#include <cstdio>
#include <string>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  // std::string problemname = "name";
  // freopen((problemname + ".in").c_str(), "r", stdin); // file io
  // freopen((problemname + ".out").c_str(), "w", stdout);
  int n;
  std::cin >> n;
  while (n--) {
    std::string s;
    std::cin >> s;
    int c = s.front();
    c -= 97;
    c /= 3;
    c += 2;
    if (c <= 7) {
      std::cout << c;
    } else if (s.front() == 's') {
      std::cout << 7;
    } else if ( s.front() == 't' or s.front() == 'u' or s.front() == 'v') {
      std::cout << 8;
    } else {
      std::cout << 9;
    }
  }
  std::cout << '\n';
  return 0;
}
