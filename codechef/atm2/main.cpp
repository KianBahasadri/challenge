#include <iostream>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  
  int t;
  std::cin >> t;
  while (t--) {
    int n;
    std::cin >> n;
    int k;
    std::cin >> k;
    long long bank = k;
    while (n--) {
      int a;
      std::cin >> a;
      if (a <= bank) {
        bank -= a;
        std::cout << '1';
      } else {
        std::cout << '0';
      }
    }
    std::cout << '\n';
  }
  return 0;
}
