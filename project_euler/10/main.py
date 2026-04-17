from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

primes = set()
count = 0
n = 10 # 17
n = 2*10**6

for i in range(2, n):
  if i % (int(n*0.05)) == 0:
    print(f"{round(i*100/n)}% complete...")

  if i in primes:
    count += i
  else:
    for p in primes:
      if i % p == 0:
        break
    else:
      primes.add(i)
      count += i

print(f"number of primes: {len(primes)}")
print(count)
