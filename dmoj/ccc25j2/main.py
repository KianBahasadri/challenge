from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

d = ii()
for _ in range(ii()):
  if input() == '+':
    d += ii()
  else:
    d -= ii()
print(d)
