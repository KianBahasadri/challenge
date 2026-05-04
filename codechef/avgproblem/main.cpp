#include <iostream>

int main() {
  int t;
  std::cin >> t;
  for (int i=0; i<t; i++) {
    double a, b, c;
    std::cin >> a;
    std::cin >> b;
    std::cin >> c;
    if ((a + b) / 2 > c) {
      std::cout << "YES" << '\n';
    } else {
      std::cout << "NO" << '\n';
    }
  }
  return 0;
}
