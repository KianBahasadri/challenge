#include <iostream>

int solution(int number) {
  int n = 0;
  for (int i=0; i<number; i++) {
    if (i % 3 == 0 | i % 5 == 0) {
      n += i;
    }
  }
  return n;
}

int main() {
  std::cout << solution(10) << '\n';
  return 0;
}
