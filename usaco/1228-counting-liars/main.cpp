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
  int n;
  std::vector<int> Gs;
  std::vector<int> Ls;
  std::cin >> n;
  for (int i=0; i<n;i++) {
    char l;
    int p;
    std::cin >> l >> p;
    if (l == 'G') {
      Gs.push_back(p);
    } else {
      Ls.push_back(p);
    }
  }


  for (int i=0; i<n;i++) {
    
    
}
