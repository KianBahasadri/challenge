from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

t = ii()
for _ in range(t):
  n = ii()
  r1 = input()
  r2 = input()
  count = 0

  i = 0
  while i < n:
    if r1[i] == r2[i]:
      pass
    elif i<n-1 and r1[i] == r1[i+1] and r2[i] == r2[i+1]:
      i += 1
      pass
    else:
      count += 1

    i += 1
  
  print(count)

