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

  for i in range(0, x+1, 4):
    first = x + (4 - x % 4) - 1
    found = ceil((n - first) / 4) + ((n+1) % 4 == 0)
    #print(i, first, "found:", found)
    count += found
  for i in range(2, x+1, 4):
    first = x + (4 - x % 4) - 3
    if first < x:
      first += 4
    if first > n:
      break
    found = ceil((n - first) / 4) + ((n+3) % 4 == 0)
    #print(i, first, "found:", found)
    count += found

  print(count)


