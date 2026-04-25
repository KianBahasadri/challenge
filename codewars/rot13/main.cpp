#include <iostream>
#include <string>
#include <cctype>

std::string rot13(std::string msg) {
  for (int i=0; i<msg.size(); i++) {
    if (std::isalpha(msg[i])) {
      bool wasupper = std::isupper(msg[i]);
      char c = std::tolower(msg[i]);
      c -= 97;
      c += 13;
      c = c % 26;
      c += 97;
      c = wasupper ? std::toupper(c) : c;
      msg[i] = c;
    }
  }
  return msg;
}

int main() {
  std::cout << rot13("Test") << '\n';
  return 0;
}
