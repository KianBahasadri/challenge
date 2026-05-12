#include <iostream>
#include <cstdio>
#include <string>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "lostcow";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);

  int x, y;
  std::cin >> x >> y;
  int travelled = 0;
  int position = x;
  for (int i=0;;i++) {
    int parity = i % 2 == 0 ? 1 : -1;
    int moveto = x + (1 << i) * parity;
    if ((moveto >= y && y >= x) || (moveto <= y && y <= x)) {
      travelled += std::abs(position - y);
      break;
    }
      
    travelled += std::abs(position - moveto);
    position = moveto;
  }
  std::cout << travelled << '\n';
  return 0;  
}
