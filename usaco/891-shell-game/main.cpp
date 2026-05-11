#include <iostream>
#include <cstdio>
#include <string>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "shell";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);

  int guess_count[3] {};
  int position[3] = {0, 1, 2};
  int n;
  std::cin >> n;
  while (n--) {
    int a, b, g;
    std::cin >> a >> b >> g;
    a--;
    b--;
    int temp = position[a];
    position[a] = position[b];
    position[b] = temp;
    g--;
    guess_count[position[g]]++;
  }
  std::cout << std::max(guess_count[0], std::max(guess_count[1], guess_count[2])) << '\n';
  return 0;
}
