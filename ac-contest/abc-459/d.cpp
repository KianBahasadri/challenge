#include <iostream>
#include <cstdio>
#include <string>
#include <algorithm>

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
    std::string s;
    std::cin >> s;
    int count[26] = {};
    for (char c: s) {
      count[c-97]++;
    }
    int sum = 0;
    int max = 0;
    for (int c: count) {
      max = std::max(max, c);
      sum += c;
    }
    if (max > (sum+1)/2) {
      std::cout << "No" << '\n';
    } else {
      std::cout << "Yes" << '\n';
      int prev_i = 999;
      for (int j=0; j < sum; j++) {
        max = 0;
        int max_i = 0;
        for (int i=0;i<26;i++) {
          if (count[i] > max && i != prev_i) {
            max = count[i];
            max_i = i;
          }
        }
        char c = max_i + 97;
        std::cout << c;
        count[max_i]--;
        prev_i = max_i;
      }
      std::cout << '\n';
    }
  }
  return 0;
}
