from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

t = ii()

for _ in range(t):
  s = input()
  doubles = 0
  for i in range(len(s)-1):
    if s[i] == s[i+1]:
      doubles += 1

  if doubles > 2:
    print("NO")
  else:
    print("YES")
