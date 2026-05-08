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
  int t;
  std::cin >> t;
  while (t--) {
    std::string s, t;
    std::cin >> s >> t;
    for (int i=0; i<5; i++) {
      if (s[i] == t[i]) {
        std::cout << 'G';
      } else {
        std::cout << 'B';
      }
    }
    std::cout << '\n';
  }
  return 0;  
}
