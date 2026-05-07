#include <iostream>
#include <cstdio>

int main() {
  std::ios_base::sync_with_stdio(false);
  std::cin.tie(NULL);
  freopen("paint.in", "r", stdin); // file io
  freopen("paint.out", "w", stdout);

  int a, b, c, d;
  std::cin >> a >> b >> c >> d;
  
  int overlap = 0;
  if (a >= c && a < d) {
    overlap = d - a;
    if (b < d) {
      overlap -= d - b;
    }
  } else if (c >= a && c < b) {
    overlap = b - c;
    if (d < b) {
      overlap -= b - d;
    }
  }
  std::cout << b - a + d - c - overlap;
  return 0;   
}
