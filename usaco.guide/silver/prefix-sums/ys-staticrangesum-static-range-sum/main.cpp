#include <iostream>
#include <vector>

int main() {
  int n;
  int q;
  std::cin >> n;
  std::cin >> q;

  std::vector<long long> prefix;
  prefix.reserve(n);

  for (int i=0; i < n; i++) {
    int x;
    std::cin >> x;
    prefix.push_back(x);
    if (i > 0) {
      prefix[i] += prefix[i-1];
    }
  }
  for (int i=0; i < q; i++) {
    long long l;
    long long r;
    std::cin >> l;
    std::cin >> r;
    if (l == 0) {
      r = r == 0 ? 1 : r; // avoid int underflow
      std::cout << prefix[r-1];
    } else {
      std::cout << prefix[r-1] - prefix[l-1];
    }
    std::cout << '\n';
  }
  return 0;
}
