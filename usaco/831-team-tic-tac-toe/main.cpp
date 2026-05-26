#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <unordered_set>
#include <algorithm>
bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "tttt";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  std::string grid[3] = {};
  for (int i=0; i<3; i++) {
    std::cin >> grid[i];
  }
  std::unordered_set<std::string> winners; 

  for (int i=0; i<3; i++) {
    winners.insert(grid[i]); 
  }
  for (int i=0; i<3; i++) {
    std::string col({grid[0][i], grid[1][i], grid[2][i]}); 
    winners.insert(col);
  }
  std::string diag1({grid[0][0], grid[1][1], grid[2][2]}); 
  std::string diag2({grid[0][2], grid[1][1], grid[2][0]}); 
  winners.insert(diag1);
  winners.insert(diag2);
  
  int one = 0, two = 0;
  std::unordered_set<std::string> counted;
  for (std::string w : winners) {
    std::sort(w.begin(), w.end());
    if (w[1] == w[2]) {
      w.erase(2, 1);
    }
    if (w[0] == w[1]) {
      w.erase(0, 1);
    }
    if (w.size() == 1 && counted.find(w) == counted.end()) {
      one++;
      counted.insert(w);
    }
    if (w.size() == 2 && counted.find(w) == counted.end()) {
      two++;
      counted.insert(w);
    }
  }
  std::cout << one << '\n' << two << '\n';
  return 0;     
}
