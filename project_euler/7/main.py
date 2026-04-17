from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

def factor(n):
  for i in range(2, n):
    if n % i == 0:
        return factor(n//i) + factor(i)
  return [n]

n = 10_001
num_primes = 0
i = 2

while num_primes < n:
  if num_primes % 100 == 0:
    print(f"calculated {num_primes} so far...")
  if len(factor(i)) == 1:
    num_primes += 1
  i += 1

print(i-1)
