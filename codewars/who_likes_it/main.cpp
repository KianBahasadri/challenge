#include <iostream>
#include <string>
#include <vector>

std::string likes(const std::vector<std::string> &names) {
  switch (names.size()) {
    case 0:
      return "no one likes this";
    case 1:
      return names[0] + " likes this";
    case 2:
      return names[0] + " and " + names[1] + " like this";
    case 3:
      return names[0] + ", " + names[1] + " and " + names[2] + " like this";
    default:
      std::string others = std::to_string(names.size() - 2);
      return names[0] + ", " + names[1] + " and " + others + " others like this";
    }
}

int main() {
  std::cout << likes({"Alex"}) << '\n';
  std::cout << likes({"Alex", "Max"}) << '\n';
  std::cout << likes({"Alex", "Jacob", "Max"}) << '\n';
  std::cout << likes({"Alex", "Jacob", "Mark", "Max"}) << '\n';
  return 0;
}
