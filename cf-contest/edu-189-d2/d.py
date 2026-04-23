from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

def xor(a, b):
  out = a
  for i in range(a+1, b+1):
    out = out^i
  return out

for _ in range(ii()):
  n, x = splii()
  count = 0
  print('-'*10)
  for i in range(1, x+1):
    for j in range(x, n+1):
      if xor(i, j) == 0:
        print(i, j)
        count += 1
      #print(f"[{i}, {j}]: {xor(i, j)}")
  print(f"count: {count}")
  print('-'*10)
