#include <iostream>
#include <string>
#include <cctype>

std::string pig_it(const std::string str) {
  std::string out;
  std::string b1; // buffer1
  std::string b2;
  for (char c: str + ' ') {
    if (!std::isalpha(c)) {
      out += b2 + b1 + c;
      b1.clear();
      b2.clear();
    } else if (b1.empty()) {
      b1 = std::string(1, c) + "ay";
    } else {
      b2 += c;
    }
  }
  out.pop_back();
  return out;
}

int main() {
  std::cout << pig_it("Pig latin is cool") << '\n';
  return 0;
}
