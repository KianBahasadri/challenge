def prime_factors(n):
  for i in range(2, n):
    if n % i == 0:
        return [i] + factor(n//i)
  return [n]

def all_factors(n):
  fs = []
  for i in range(1, n+1):
    if n % i == 0:
      fs.append(i)
  return fs

