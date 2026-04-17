def factor(n):
  for i in range(2, n):
    if n % i == 0:
        return factor(n//i) + factor(i)
  return [n]

