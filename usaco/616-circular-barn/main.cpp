#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "cbarn";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  int n;
  std::cin >> n;
  std::vector<int> r;
  int cows = 0;
  while (n--) {
    int x;
    std::cin >> x;
    r.push_back(x);
    cows += x;
  }
  int min = 999999999;
  for (int i=0;i < r.size(); i++) {
    int walked = 0;
    int cows_left = cows;
    for (int j=0;j < r.size(); j++) {
      cows_left -= r[(i + j) % r.size()];
      walked += cows_left;
    }
    min = std::min(walked, min);
  }
  std::cout << min << '\n';
  return 0;  
}
