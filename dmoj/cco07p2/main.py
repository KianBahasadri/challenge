from sys import exit
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())

n = ii()
_set = set()

for _ in range(n):
  s = input().split()
  s = int(''.join(s))
  if s not in _set:
    _set.add(s)
  else:
    print("Twin snowflakes found.")
    exit()
 
print(_set)

for ss in _set:
  _set.remove(ss)
  print(ss)
  for i in range(6):
    s = str(ss)
    new = int((s[i:] + s[:i]))
    new2 = int((s[i:] + s[:i])[::-1])
    print(new, new2)
    if new in _set or new2 in _set:
      print("Twin snowflakes found.")
      exit()
  _set.add(ss)

print("No two snowflakes are alike.")

