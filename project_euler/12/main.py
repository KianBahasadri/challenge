from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

def factor(n):
  for i in range(2, n):
    if n % i == 0:
        return [n] + factor(n//i) + factor(i)
  return [n]

count = 0
for i in range(10**10):
  count += i
  fs = set(factor(count) + [1])
  if i % 500 == 0:
    print(i, count, sorted(list(fs)))
  if len(fs) > 500:
    print(i)
    break
