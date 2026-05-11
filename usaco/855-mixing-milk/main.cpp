#include <iostream>
#include <cstdio>
#include <string>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "mixmilk";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);

  int c[3];
  int m[3];
  std::cin >> c[0] >> m[0];
  std::cin >> c[1] >> m[1];
  std::cin >> c[2] >> m[2];
  
  for (int i = 0; i < 100; i++) {
    int n = (i+1) % 3;
    int pour = std::min(m[i % 3], c[n] - m[n]);
    m[n] += pour;
    m[i % 3] -= pour;
  }
  for (int i=0; i< 3; i++) {
    std::cout << m[i] << '\n';
  }
  return 0;
}
