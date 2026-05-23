#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  // std::string problemname = "name";
  // freopen((problemname + ".in").c_str(), "r", stdin); // file io
  // freopen((problemname + ".out").c_str(), "w", stdout);
  int n, q;
  std::cin >> n >> q;
  std::vector<int> blocks(n, 0);
  std::vector<int> count(3*100000+1, 0);
  int removed = 0;
  count[0] = n;
  while (q--) {
    int t, x;
    std::cin >> t >> x;
    if (t == 1) {
      x -= 1;
      count[blocks[x]] -= 1;
      blocks[x] += 1;
      count[blocks[x]] += 1;
      if (count[removed] == 0) {
        removed += 1;
      }
    } else {
      int sum = 0;
      for (int i=x+removed; i < count.size(); i++) {
        sum += count[i];
      }
      std::cout << sum << '\n';
    }
  }
  return 0;  
}
