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

def remove(adj_list):
  for adj in adj_list:
    if [x for x in adj_list[adj] if x in adj_list] == []:
      del adj_list[adj]
      return remove(adj_list)
  return adj_list

print(len(remove(adj_list)))

