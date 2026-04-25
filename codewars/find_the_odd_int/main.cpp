#include <iostream>
#include <vector>
#include <unordered_set>

int findOdd(const std::vector<int>& numbers){
  std::unordered_set<int> set;
  for (int n : numbers) {
    if (set.count(n)) {
      set.erase(n);
    } else {
      set.insert(n);
    }
  }
  return *set.begin();
}

int main() {
  std::cout << findOdd(std::vector<int>{20,1,-1,2,-2,3,3,5,5,1,2,4,20,4,-1,-2,5}) << '\n';
  return 0;
}
