from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

for _ in range(ii()):
  n, m = splii()
  a = splii()
  last = 0
  last_count = 0
  for ai in a:
    if ai == last:
      last_count += 1
      if last_count == m:
        print("NO")
        break
    else:
      last = ai
      last_count = 1
  else:
    print("YES")
