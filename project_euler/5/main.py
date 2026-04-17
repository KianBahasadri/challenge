from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

# im gonna be so fr dawg if you can even understand what the fuck
# i was doing by reading this, thats pretty impressive already

factors = [0]*21

def factor(n):
  for i in range(2, n):
    if n % i == 0:
        return factor(n//i) + factor(i)
  return [n]

for i in range(2,21):
  numfactors = factor(i)
  for f in numfactors:
    if factors[f] < numfactors.count(f):
      factors[f] = numfactors.count(f)

print(factors)

LCM = 1
for i in range(2,21):
  LCM *= i**factors[i]
print(LCM)


