#include <iostream>
#include <string>

int digital_root(int n) {
    int sum = 0;
    std::string strnum = std::to_string(n);
    for (char c: strnum) {
      sum += c - '0';
    }
    if (sum > 9) {
      return digital_root(sum);
    }
    return sum;
}

int main() {
  std::cout << digital_root(9) << '\n';
  std::cout << digital_root(167346) << '\n';
  return 0;
}
