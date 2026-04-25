#include <iostream>
#include <string>

std::string spinWords(const std::string &str) {
  std::string out;
  std::string buffer;
  for (char c: str + ' ') {
    if (c != ' ') {
      buffer += c;
    } else {
      if (buffer.size() > 4) {
        out += std::string(buffer.rbegin(), buffer.rend());
      } else {
        out += buffer;
      }
      out += ' ';
      buffer.clear();
    }
  }
  out.pop_back();
  return out;
}

int main() {
  std::cout << spinWords("Pizza is the best vegetable") << '\n';
  return 0;
}
