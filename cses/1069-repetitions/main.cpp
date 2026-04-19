#include <iostream>
#include <string>

int main() {
  std::string seq;
  std::cin >> seq;
  int max = 1;
  int count = 1;
  for (size_t i=1; i < seq.size(); i++) {
    if (seq[i] == seq[i-1]) {
      count += 1;
      max = count > max ? count : max;
    } else {
      count = 1;
    }
  }
  std::cout << max;
  return 0;
}
