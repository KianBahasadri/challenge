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
  int n;
  std::cin >> n;
  int m = n;
  std::vector<int> x;
  while (m--) {
    int val;
    std::cin >> val;
    x.push_back(val);
  }
  m = n;
  std::vector<int> y;
  while (m--) {
    int val;
    std::cin >> val;
    y.push_back(val);
  }
  int max = 0;
  for (int i=0; i<n;i++) {
    for (int j=0; j<n;j++) {
      int distance = (x[i] - x[j]) * (x[i] - x[j]);
      distance += (y[i] - y[j]) * (y[i] - y[j]);
      max = std::max(distance, max);
    }
  }
  std::cout << max << '\n';
  return 0;  
}
