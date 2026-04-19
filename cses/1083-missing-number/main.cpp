#include <iostream>
#include <vector>

int main() {
  int n;
  std::cin >> n;
  std::vector<int> a(n);
  int num;
  for (int i=0; i<n;i++) {
    std::cin >> num;
    a[num-1] = 1;
  }
  for (int i=0; i<n;i++) {
    if (a[i] == 0) {
      std::cout << i+1;
      break;
    }
  }
  return 0;
}
