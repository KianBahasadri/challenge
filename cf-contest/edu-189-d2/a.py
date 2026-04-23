from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

t = ii()

for _ in range(t):
  x, y = splii()
  for n in range(x, y, x):
    if y % n != 0:
      print("YES")
      break
  else:
    print("NO")
