ii = lambda: int(input())

h = []
n = ii()
for i in range(n):
  h.append(ii())
 
count = 0
for i in range(n):
  count += h[i] == h[(i - (n // 2) % n)]

print(count)
     
