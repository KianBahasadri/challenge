from sys import exit
from collections import defaultdict
from math import ceil
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

for _ in range(ii()):
  n, x = splii()
  count = 0

  first = x + (4 - x % 4) - 1
  found = ceil((n - first) / 4) + ((n+1) % 4 == 0)
  count += found * ((x+1) // 4 + 1)
  print(f"a: {found} * {((x+1) // 4 + 1)}")

  first = x + (4 - x % 4) - 3
  if first < x:
    first += 4
  if first > n:
    break
  found = ceil((n - first) / 4) + ((n+3) % 4 == 0)
  count += found * (((x+1 - 2) // 4) + 1)
  print(f"b: {found} * {(((x+1 - 2) // 4) + 1)}")

  print(count)


