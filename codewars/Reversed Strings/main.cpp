#include <iostream>
#include <string>
#include <algorithm>

std::string reverseString(const std::string &str) {
  return std::string(str.rbegin(), str.rend());
}

int main() {
  std::cout << reverseString("hello") << '\n';
  return 0;
}
