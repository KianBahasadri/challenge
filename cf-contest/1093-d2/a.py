from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

for _ in range(ii()):
  n = ii()
  a = list(splii())
  count = [0]*101
  for ai in a:
    count[ai] += 1
  if any([x > 1 for x in count]):
    print(-1)
  else:
    a.sort(reverse=True)
    print(' '.join(map(str, a)))

