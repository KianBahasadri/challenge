#include <iostream>
#include <cstdio>
#include <string>
#include <vector>
#include <list>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  std::string problemname = "censor";
  freopen((problemname + ".in").c_str(), "r", stdin); // file io
  freopen((problemname + ".out").c_str(), "w", stdout);
  std::string s, t;
  std::cin >> s >> t;
  std::list<char> l(s.begin(), s.end());
  std::list<char>::iterator i = l.begin();
  while (i != l.end()) {
    bool found = true;
    std::list<char>::iterator ii = i;
    for (int j=0; j < t.size(); j++) {
      if (*ii != t[j]) {
        found = false;
        break;
      }
      ii++;
    }
    if (found) {
      i = l.erase(i, ii);
      int j = t.size();
      while (j-- && i != l.begin()) {
        i--;
      }
    } else {
      i++;
    }
  }
  std::string out(l.begin(), l.end());
  std::cout << out << '\n';
  return 0;
}
