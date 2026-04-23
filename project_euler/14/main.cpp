#include <iostream>

int main() {
  unsigned long long max[2] {};
  for (int i=2; i<1000000; i++) {
    unsigned long long n = i;
    unsigned long long iterations = 0;
    while (n != 1) {
      if (n % 2 == 0) {
        n /= 2;
      } else {
        n = 3*n + 1;
      }
      iterations += 1;
    }
    if (iterations > max[0]) {
      max[0] = iterations;
      max[1] = i;
    }
  }
  
  std::cout << max[1] << '\n';
  return 0;
}
