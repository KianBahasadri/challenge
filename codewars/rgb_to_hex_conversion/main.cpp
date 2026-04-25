#include <iostream>
#include <string>
#include <sstream>
#include <cctype>

std::string rgb_to_hex(int r, int g, int b) {
  std::string hex;
  for (int n : {r, g, b}) {
    if (n < 0) {
      n = 0;
    } else if (n > 255) {
      n = 255;
    }
    std::stringstream stream;
    stream << std::hex << n;
    std::string result = stream.str();
    if (result.size() == 1) {
      hex += '0';
    }
    hex += result;
  }
  for (int i=0; i< hex.size(); i++) {
    hex[i] = std::toupper(hex[i]);
  }
  return hex;
}
int main() {
  std::cout << rgb_to_hex(255,255,255) << '\n';
  std::cout << rgb_to_hex(  1,  2,  3) << '\n';
  std::cout << rgb_to_hex(0,0,0) << '\n';
  std::cout << rgb_to_hex(-20,275,125) << '\n';
  return 0;
}
