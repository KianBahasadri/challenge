#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "blist";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);

  int n;
  std::cin >> n;
  std::vector<int> count(1001, 0);
  while(n--) {
    int si, ti, bi;
    std::cin >> si >> ti >> bi;
    count[si] += bi;
    count [ti] -= bi;
  }
  int max = 0;
  int curr = 0;
  for (int b: count) {
    curr += b;
    max = std::max(max, curr);
  }
  std::cout << max << '\n';
  return 0;
}
