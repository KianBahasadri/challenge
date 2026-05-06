#include <iostream>
#include <vector>

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  
  int t;
  std::cin >> t;
  while (t--) {
    int n;
    std::cin >> n;
    std::vector<long long> a;
    a.reserve(n);
    while (n--) {
      int ai;
      std::cin >> ai;
      a.push_back(ai);
    }
    
    int count = a.back() > 0;

    for (int i=a.size()-2; i > -1; i--) {
      if (a[i+1] > 0) {
        a[i] += a[i+1];
      }
      if (a[i] > 0) {
        count++;
      }
    }
    std::cout << count << '\n';
  }
  return 0;
}
