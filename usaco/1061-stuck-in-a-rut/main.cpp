#include <iostream>
#include <cstdio>
#include <string>
#include <vector>

bool isvowel(char v) { return (0x208222>>(v&0x1f))&1; }
// https://stackoverflow.com/a/47846874

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  int n;
  std::cin >> n;
  struct Cow {
    char f;
    int x, y;
  }
  std::vector<Cow> cow(n);
  std::vector<int> count(n, 0);
  for(int i=0; i<n;i++) {
    std::cin >> cow[i].f >> cow[i].x >> cow[i].y;
  }
  while (n) {
    for(int i=0; i<n;i++) {
      int collisions = 0;
      for(int j=0; j<n;j++) {
        if (cow[i].f == 'E') {
          if (cow[j].x > cow[i].f
      
    
    
    
}
