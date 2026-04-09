az = 'abcdefghijklmnopqrstuvwxyz'
ii = lambda: int(input())

t, n = map(int, input().split())

for i in range(t):
  alph = {x: 0 for x in az}
  s = input()
  for l in s:
    alph[l] += 1
  for i in range(n-1):
    curr = alph[s[i]] <= 1
    _next = alph[s[i+1]] <= 1
    if curr == _next:
      print('F')
      break
  else:
    print('T')


