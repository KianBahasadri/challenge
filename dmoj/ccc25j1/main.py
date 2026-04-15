from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

n = ii()
c = ii()
p = ii()
print("yes" if c * p - n >= 0 else "no")
