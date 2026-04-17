from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

# max length of a triangle side is perimeter / 2

n = 12 # 3 + 4 + 5
n = 1000

for i in range(1, n//2+1):
  for j in range(1, n//2+1):
    k = n - i - j
    if i**2 + j**2 == k**2:
      print(i, j, k)
      print(i*j*k)
      exit()
