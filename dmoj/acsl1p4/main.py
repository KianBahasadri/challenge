from sys import exit
from collections import defaultdict
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())
# --- Boilerplate ---

n, k = splii()
adj_list = { i:[] for i in range(n+1)}
adj_list2 = { i:[] for i in range(n+1)}

for _ in range(k):
  a, b, sa, sb = splii()
  if sa > sb:
    adj_list[a].append(b)
    adj_list2[b].append(a)
  else:
    adj_list[b].append(a)
    adj_list2[a].append(b)

def remove(adj_list):
  for adj in adj_list:
    if [x for x in adj_list[adj] if x in adj_list] == []:
      del adj_list[adj]
      return remove(adj_list)
  return adj_list

a1 = remove(adj_list)
a2 = remove(adj_list2)

count = len(set(a1).intersection(set(a2)))

print(count)

