#include <iostream>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  int t;
  std::cin >> t;
  while (t--) {
    int a1, b1, c1;
    std::cin >> a1;
    std::cin >> b1;
    std::cin >> c1;
    int a2, b2, c2;
    std::cin >> a2;
    std::cin >> b2;
    std::cin >> c2;

    if (a1+b1+c1 > a2+b2+c2) {
      std::cout << "Dragon\n";
    } else if (a1+b1+c1 < a2+b2+c2) {
      std::cout << "Sloth\n";
    } else if (a1 > a2) {
      std::cout << "Dragon\n";
    } else if (a1 < a2) {
      std::cout << "Sloth\n";
    } else if (b1 > b2) {
      std::cout << "Dragon\n";
    } else if (b1 < b2) {
      std::cout << "Sloth\n";
    } else if (c1 > c2) {
      std::cout << "Dragon\n";
    } else if (c1 < c2) {
      std::cout << "Sloth\n";
    } else {
      std::cout << "tie\n";
    }
  }
  return 0;
}
