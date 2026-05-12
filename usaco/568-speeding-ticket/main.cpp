#include <iostream>
#include <cstdio>
#include <string>
#include <array>

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
  std::array<std::array<int, 2>, n> roads;
  std::array<std::array<int, 2>, m> speeds;
  for (int i=0; i < n;i++) {
    std::cin >> roads[i][0] >> roads[i][1];
    if (i > 0) {
      roads[i][0] += roads[i-1][0];
    }
  }
  for (int i=0; i < m;i++) {
    std::cin >> speeds[i][0] >> speeds[i][1];
    if (i > 0) {
      speeds[i][0] += speeds[i-1][0];
    }
  }
  int max = 0;
  int travelled = 0;
  for (int i=0; i < m;) {
    if (travelled < roads[i]) {
      
      


  
}
