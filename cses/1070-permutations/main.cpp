#include <iostream>

int main() {
  int n;
  std::cin >> n;

  if (n < 5) {
    std::cout << "NO SOLUTION";
    return 0;
  }

  if (n % 2 == 0) {
    std::cout << n << ' ';
    n -= 1;
  }

  for (int i=0; i!=n; i=(i+2)%n) {
    std::cout << i+1 << ' ';
  }
  return 0;
}
