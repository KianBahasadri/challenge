from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

count, a, b = 0, 1, 2
count += b
while not b > 4e6:
  if (a + b) % 2 == 0:
    count += a + b
  a, b = b, a + b
print(count)
