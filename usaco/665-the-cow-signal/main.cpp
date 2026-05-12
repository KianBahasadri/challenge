#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "cowsignal";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);

  int m, n, k;
  std::cin >> m >> n >> k;
  std::vector<std::vector<char>> a;
  for (int i=0; i<m;i++) {
    a.push_back(std::vector<char>());
    for (int j=0; j<n;j++) {
      char c;
      std::cin >> c;
      a[i].push_back(c);
    }
  }
  for (int i=0; i<m;i++) {
    std::string line;
    for (int j=0; j<n;j++) {
      for(int x=0;x<k;x++) {
        line += a[i][j];
      }
    }
    for(int x=0;x<k;x++) {
      std::cout << line << '\n';
    }
  }
  return 0;
}
