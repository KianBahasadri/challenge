from sys import exit, setrecursionlimit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---
n = 600851475143

def factor(n):
  for i in range(2, n):
    if n % i == 0:
        return factor(n//i) + factor(i)
  return [n]

print(factor(n))
