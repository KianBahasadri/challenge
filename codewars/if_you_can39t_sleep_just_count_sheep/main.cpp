#include <iostream>
#include <string>

std::string countSheep(int number) {
  if (number == 0) {
    return "";
  }
  return countSheep(number-1) + std::to_string(number) + " sheep...";
}

int main() {
  std::cout << countSheep(5) << '\n';
  return 0;
}
