#include <iostream>
#include <string>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  
  int t;
  std::cin >> t;
  while (t--) {
    int n;
    std::cin >> n;
    std::string s;
    std::cin >> s;
    std::string easy = "YES";
    for (int i=0; i < n-3; i++) {
      if (!(isvowel(s[i]) || isvowel(s[i+1]) || isvowel(s[i+2]) || isvowel(s[i+3]))) {
        easy = "NO";
        break;
      }
    }
    std::cout << easy << '\n';
  }
  return 0;
}
