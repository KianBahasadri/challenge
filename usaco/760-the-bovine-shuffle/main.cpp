#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "shuffle";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);

  int n;
  std::cin >> n;
  std::vector<int> a(n);
  std::vector<int> b(n);
  std::vector<int> cows(n);
  std::vector<int> next(n);
  for (int i=0; i<n;i++) {
    std::cin >> a[i];
  }
  for (int i=0; i<n;i++) {
    std::cin >> cows[i];
  }

  for (int i=0; i<n;i++) {
    for (int j=0; j<n;j++) {
      if (a[j] == i+1) {
        b[i] = j+1;
        break;
      }
    }
  }
        
  for (int j=0; j<3;j++) {
    for (int i=0; i<n;i++) {
      next[b[i]-1] = cows[i];
    }
    cows = next;
  }

  for (int i=0; i<n;i++) {
    std::cout << cows[i] << '\n';
  }
  return 0;
}
