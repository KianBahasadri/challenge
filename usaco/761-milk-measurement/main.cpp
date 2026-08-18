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
  std::cin >> n;
  std::array<std::pair<std::string, int>, 101> log;
  for (int i = 0; i < n; i++) {
    int day, amnt;
    std::string name;
    std::cin >> day >> name >> amnt;
    log[day] = std::pair<name, amnt>;
  }
  std::sort(log);
  std::unordered_map<std::pair<std::string, int>> output = {{"Bessie", 7}, {"Elsie", 7}, {"Mildred", 7}};
  int count = 0;
  std::
  for (int i = 0; i < 101; i++) {
    if (log[i][0]) {
      output[log[i].first] += log[i].second;
    }
  std::cout << count << '\n';
  return 0;
}
