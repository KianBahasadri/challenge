#include <iostream>
#include <vector>

std::vector<int> move_zeroes(const std::vector<int>& input) {
  std::vector<int> v2;
  int zeros = 0;
  for (int x : input) {
    if (x) {
      v2.push_back(x);
    } else {
      zeros++;
    }
  }
  v2.insert(v2.end(), zeros, 0);
  return v2;
}

int main() {
  std::vector v = move_zeroes(std::vector<int>{1, 2, 0, 1, 0, 1, 0, 3, 0, 1});
  for (int x: v) {
    std::cout << x << ' ';
  }
  return 0;
}
