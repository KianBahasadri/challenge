from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

n = ii()
while n != 1:
  print(n, end=' ')
  if n % 2:
    n = n * 3 + 1
  else:
    n = n // 2
print(1)
  
