#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "blocks";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  int n;
  std::cin >> n;
  int count[26] = {};
  while (n--) {
    std::string s1, s2;
    std::cin >> s1 >> s2;
    int s1c[26] = {};
    int s2c[26] = {};
    for (char c: s1) { s1c[c-97]++; }
    for (char c: s2) { s2c[c-97]++; }
    for (int i=0; i<26;i++ ) {
      count[i] += std::max(s1c[i], s2c[i]);
    }
  }
  for (int i=0; i<26;i++ ) {
    std::cout << count[i] << '\n';
  }
  return 0;
}
