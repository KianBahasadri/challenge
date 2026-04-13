from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

adj_list = defaultdict(list)
n, k = splii()
for _ in range(k):
  a, b, sa, sb = splii()
  if sa > sb:
    adj_list[a].append(b)
    adj_list.setdefault(b, [])
  else:
    adj_list[b].append(a)
    adj_list.setdefault(a, [])

while True:
  for adj in adj_list:
    if adj_list[adj] == []:
      del adj_list[adj]
      for adj2 in adj_list:
        adj_list[adj2] = [x for x in adj_list[adj2] if x != adj]
      break
  else:
    break

print(len(adj_list))

  

