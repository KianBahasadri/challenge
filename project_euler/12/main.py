from sympy import factorint
from math import comb

def factor(n):
  for i in range(2, n):
    if n % i == 0:
        return [n] + factor(n//i) + factor(i)
  return [n]

for i in range(1, 15):
  n = int(i * (2*i + 1))
  n2 = int(i * (2*i - 1))

  fs1 = set(factor(n) + [1])
  fs2 = set(factor(n2) + [1])

  print((i, (2*i - 1)), n2, sorted(list(fs2)))
  print((i, (2*i + 1)), n, sorted(list(fs1)))
