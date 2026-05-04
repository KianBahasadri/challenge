#include <iostream>

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);

  int t;
  std::cin >> t;
  while (t--) {
    int n, x;
    std::cin >> n;
    std::cin >> x;
    int extra = (n % 6) != 0 ? 1 : 0;
    std::cout << (n/6 + extra) * x << '\n';
  }
  return 0;
}
