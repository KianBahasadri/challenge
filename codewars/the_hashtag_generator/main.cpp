#include <iostream>
#include <optional>
#include <string>
#include <cctype>

std::optional<std::string> generate_hashtag(const std::string& str) {
  if (str.empty()) {
    return std::nullopt;
  }

  std::string buffer = "#";
  bool caps = true;

  for (int i=0; i < str.size(); i++) {
    if (std::isalpha(str[i])) {
      buffer += caps ? std::toupper(str[i]) : std::tolower(str[i]);
      caps = false;
    } else {
      caps = true;
    }
  }
  if (buffer.size() > 140 or buffer.size() == 1) {
    return std::nullopt;
  } else {
    return buffer;
  }
}
int main() {
  std::cout << generate_hashtag("Do We have A Hashtag").value() << '\n';
  std::cout << generate_hashtag(std::string(200, ' ')).value() << '\n';
  return 0;
}
