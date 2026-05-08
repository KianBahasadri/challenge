#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int popmin(std::vector<int>& a) {
  int min_i = 0;
  for (int i=0; i < a.size(); i++) {
    if (a[i] < a[min_i]) {
      min_i = i;
    }
  }
  int x = a[min_i];
  a.erase(a.begin() + min_i);
  return x;
}


int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  // std::string problemname = "name";
  // freopen((problemname + ".in").c_str(), "r", stdin); // file io
  // freopen((problemname + ".out").c_str(), "w", stdout);
  std::vector<int> a;
  int i = 7;
  while (i--) {
    int x;
    std::cin >> x;
    a.push_back(x);
  }
  int aa = popmin(a);
  int bb = popmin(a);
  int maybec = popmin(a);
  int cc;
  if (aa + bb == maybec) {
    cc = popmin(a);
  } else {
    cc = maybec;
  }
  std::cout << aa << " " << bb << " " << cc << '\n';
  return 0;  
}
