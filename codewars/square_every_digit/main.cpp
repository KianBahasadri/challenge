#include <iostream>
#include <string>

int square_digits(int num) {
  std::string out;
  for (char c : std::to_string(num)) {
    int digit = c - '0';
    out += std::to_string(digit * digit);
  }
 return std::stoi(out);
}

int main() {
  std::cout << square_digits(3212) << '\n';
  return 0;
}
