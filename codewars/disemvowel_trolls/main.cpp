#include <iostream>
# include <string>
#include <cctype>

std::string disemvowel(const std::string& str) {
  std::string x;
  for (char c: str) {
    if (!std::isalpha(c) || (~0x208222>>(c&0x1f)&1)) {
      x += c;
    }
  }
  return x;
}

int main() {
  std::cout << disemvowel("This website is for losers LOL!") << '\n';
  return 0;
}
