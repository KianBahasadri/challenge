from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

pals = []

for i in range(900, 1000):
  for j in range(900, 1000):
    if str(i*j) == str(i*j)[::-1]:
      pals.append(i*j)

print(max(pals))
