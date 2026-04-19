#include <iostream>
#include <vector>

int main() {
  unsigned long long moves = 0;
  int n;
  std::cin >> n;
  int last;
  int curr;
  std::cin >> last;
  for (int i=0; i<n-1; i++) {
    std::cin >> curr;
    if (curr < last) {
      moves += last - curr;
    } else {
      last = curr;
    }
  }
  std::cout << moves;
  return 0;
}
