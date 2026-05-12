#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "speeding";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);

  int n, m;
  std::cin >> n >> m;
  std::vector<int> limits;
  std::vector<int> speeds;
  for (int i=0; i < n;i++) {
    int segment, speed;
    std::cin >> segment >> speed;
    for (int j=0; j<segment;j++) {
      limits.push_back(speed);
    }
  }
  for (int i=0; i < m;i++) {
    int segment, speed;
    std::cin >> segment >> speed;
    for (int j=0; j<segment;j++) {
      speeds.push_back(speed);
    }
  }
  int max = 0;
  for (int i=0; i < 100;i++) {
      max = std::max(max, speeds[i]-limits[i]);
  }
  std::cout << max << '\n';
  return 0;
}
