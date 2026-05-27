#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <climits>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "mowing";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  int n;
  std::vector<std::vector<int>> grid(2001, std::vector<int>(2001, 0));
  int pos[2] = {1000, 1000};
  int x = INT_MAX;
  int t = 0;
  std::cin >> n;
  while (n--) {
    char f;
    int s, step[2] = {0, 0};
    std::cin >> f >> s;
    if (f == 'N') {
      step[1] = -1;
    } else if (f == 'S') {
      step[1] = 1;
    } else if (f == 'E') {
      step[0] = 1;
    } else if (f == 'W') {
      step[0] = -1;
    }
    while (s--) {
      t++;
      pos[0] += step[0];
      pos[1] += step[1];
      if (grid[pos[0]][pos[1]]) {
        x = std::min(t - grid[pos[0]][pos[1]], x);
      }
      grid[pos[0]][pos[1]] = t;
    }
  }
  x = x == INT_MAX? -1 : x;
  std::cout << x << '\n';
  return 0;
}
