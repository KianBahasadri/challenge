#include <iostream>
#include <string>
#include <cctype>

std::string abbrevName(std::string name) {
  for (int i=0;;i++) {
    if (name[i] == ' ') {
      std::string result;
      result += std::toupper(name[0]);
      result += '.';
      result += std::toupper(name[i+1]);
      return result;
    }
  }
}

int main() {
  std::cout << abbrevName("Kian Bahasadri") << '\n';
  return 0;
}
