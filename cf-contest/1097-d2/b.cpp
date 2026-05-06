#include <iostream>

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  
  int t;
  std::cin >> t;
  while (t--) {
    int n;
    std::cin >> n;
    int max = -1;
    int bucket[200000 + 1] = {};
    for (int i=0; i<n; i++) {
      int x;
      std::cin >> x;
      max = x > max ? x : max;
      if (x <= 200000) {
        bucket[x] = 1;
      }
    }
    int mexican = 0;
    int skip = 0;
    for (int i=0; i<n+skip; i++) {
      if (bucket[i] == 0) {
        mexican += i*(n-i);
        break;
      }
      if (i == max) {
        skip = 1;
        i++;
        if (max == 0) {
          // bullshit edge case
          mexican += 1;
          i -= 1;
          continue;
        }
      }
      mexican += i;
    }
    std::cout << max * n + mexican << '\n';
  }
  return 0;
}
