from sys import exit
from array import array
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())

w, h = splii()
n = ii()
dp = [array('I', [x * y for y in range(601)]) for x in range(601)]

for _ in range(n):
  x, y = splii()
  dp[x][y] = 0

#breakpoint()

for x in range(w+1):
  for y in range(h+1):
    best = dp[x][y]
    for i in range(x):
      test = dp[i][y] + dp[x-i][y]
      if test < best:
        dp[x][y] = test
        best = test
    for i in range(y):
      test = dp[x][i] + dp[x][y-i]
      if test < best:
        dp[x][y] = test
        best = test

print(dp[w][h])
