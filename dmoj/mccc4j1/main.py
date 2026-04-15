from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

tf, tm, tb = splii()
f, m, b = splii()
print(f + m + b, f*tf + m*tm + b*tb)
