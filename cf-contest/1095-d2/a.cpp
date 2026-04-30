#include <iostream>

int main() {
  int t = 0;
  std::cin >> t;
  for (int i=0; i < t; i++) {
    int sum = 0;
    int n = 0;
    std::cin >> n;
    for (int j=0; j<n; j++) {
      int aj = 0;
      std::cin >> aj;
      if ( aj == 1 ) {
        continue;
      }
      sum += aj;
    }
    sum = sum > 0 ? sum : 1;
    std::cout << sum % 676767677;
  }
  return 0;
}
