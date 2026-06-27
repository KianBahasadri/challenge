#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <unordered_set>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  // std::string problemname = "name";
  // freopen((problemname + ".in").c_str(), "r", stdin); // file io
  // freopen((problemname + ".out").c_str(), "w", stdout);
  int n, m;
  std::cin >> n >> m;
  std::vector<int> birds(n, 0);
  std::vector<int> colors(n+1, 0);
  int count_colors = 0;
  // on the ith day, the following changes happened -> [bird_i became colour]
  std::vector<std::vector<std::vector<int>>> days;
  for (int i = 0; i < m; i++) {
    days.push_back(std::vector<std::vector<int>>());
  }
  for (int i = 0; i < n; i++) {
    int a, d, b;
    std::cin >> a >> d >> b;
    birds[i] = a;
    if (colors[a] == 0) {
      count_colors++;
    }
    colors[a]++;
    days[d-1].push_back(std::vector<int>{i, b});
  }
  for (int i = 0; i < m; i++) {
    for (std::vector<int> change : days[i]) {
      colors[birds[change[0]]]--;
      if (colors[birds[change[0]]] == 0) {
        count_colors--;
      }
      if (colors[change[1]] == 0) {
        count_colors++;
      }
      colors[change[1]]++;
      birds[change[0]] = change[1];
    }
    std::cout << count_colors << '\n';
  }
  return 0;
}
