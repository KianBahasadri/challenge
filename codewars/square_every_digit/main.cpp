#include <iostream>
#include <string>
#include <cmath>

int square_digits(int num) {
  std::string out;
  for (char c: std::to_string(num)) {
    out += std::to_string(std::pow(c - '0', 2));
  }
 return std::stoi(out);
}

int main() {
  std::cout << square_digits(3212) << '\n';
  return 0;
}
