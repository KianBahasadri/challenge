ii = lambda: int(input())
n = ii()
top = {-1:0, -2:0, -3:0}

for _ in range(n):
  score = ii()
  if score in top:
    top[score] += 1
  elif score > min(top.keys()):
    top[score] = 1
    del top[min(top.keys())]
print(min(top.keys()), top[min(top.keys())])
