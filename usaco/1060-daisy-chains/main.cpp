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
  std::vector<int> flowers;
  while(n--) {
    int x;
    std::cin >> x;
    flowers.push_back(x);
  }
  int count = 0;
  for (int i=0; i < flowers.size(); i++) {
    for (int j=i; j < flowers.size(); j++) {
      double avg = 0;
      for (int k=i; k <= j; k++) {
        avg += flowers[k];
      }
      int d = j == i ? 1 : j - i + 1;
      avg /= d;
      for (int k=i; k <= j; k++) {
        if (avg == flowers[k]) {
          //std::cout << i << ' ' << j << '\n';
          count++;
          break;
        }
      }
    }
  }
  std::cout << count << '\n';
  return 0;
}
