#include <iostream>

unsigned long long fact(int n) {
  int i = 1;
  while (n > 1) {
    i *= n;
    n--;
  }
  return i;
}

unsigned long long choose(int n, int r) {
 return fact(n) / (fact(r) * fact(n - r));
}

int main() {
  std::cout << choose(4, 2) << "--";
  std::cout << choose(20+20, 20) << '\n';
  return 0;
}
