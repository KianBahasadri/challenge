#include <iostream>
#include <cstdio>
#include <string>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "word";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);

  int n, k;
  std::cin >> n >> k;
  int line = 0;
  while (n--) {
  std::string word;
  std::cin >> word;
  if (line + word.size() > k) {
    std::cout << '\n';
    line = 0;
  }
  if (line) {
    std::cout << ' ';
  }
  std::cout << word;
  line += word.size();
  }
  return 0;  
}
