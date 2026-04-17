from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

n = 100
sumsquare = sum([x**2 for x in range(n+1)])
squaresum = sum([x for x in range(n+1)])**2
print(squaresum - sumsquare)
