#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "diamond";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  int n, k;
  std::cin >> n >> k;
  std::vector<int> d(10001, 0);
  while (n--) {
    int x;
    std::cin >> x;
    d[x]++;
  }
  int count = 0;
  for (int i=0;i <= k && i < d.size(); i++) {
    count += d[i];
  }
  int _max = count;
  for(int i=k+1; i < d.size(); i++) {
    count -= d[i-k-1];
    count += d[i];
    _max = std::max(_max, count);
  }
  std::cout << _max << '\n';
  return 0;
}
