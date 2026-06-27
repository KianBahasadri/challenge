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
  int h, w;
  std::cin >> h >> w;
  std::vector<std::vector<char>> c(h, std::vector(w, '_'));
  for (int i=0; i < h; i++) {
    for (int j=0; j < w; j++) {
      std::cin >> c[i][j];
    }
  }

  bool found_black = false;
  while (!found_black) {
    found_black = false;
    for (int i=0; i < w; i++) {
      if (c[0][i] == '#') {
        found_black = true;
        break;
      }
    }
    if (! found_black) {
      c.erase(c.begin());
      h--;
      continue;
    }
    found_black = false;
    for (int i=0; i < w; i++) {
      if (c[h-1][i] == '#') {
        found_black = true;
        break;
      }
    }
    if (! found_black) {
      c.pop_back();
      h--;
      continue;
    }
    found_black = false;
    for (int i=0; i < h; i++) {
      if (c[i][0] == '#') {
        found_black = true;
        break;
      }
    }
    if (! found_black) {
      for (int i=0; i < h; i++) {
        c[i].erase(c[i].begin());
      }
      w--;
      continue;
    }
    found_black = false;
    for (int i=0; i < h; i++) {
      if (c[i][w-1] == '#') {
        found_black = true;
        break;
      }
    }
    if (! found_black) {
      for (int i=0; i < h; i++) {
        c[i].pop_back();
      }
      w--;
      continue;
    }
  }

  for (int i=0; i < h; i++) {
    for (int j=0; j < w; j++) {
      std::cout << c[i][j];
    }
    std::cout << '\n';
  }
  return 0;
}
