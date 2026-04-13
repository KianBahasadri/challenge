from sys import exit
az = 'abcdefghijklmnopqrstuvwxyz'
splii = lambda: map(int, input().split())
ii = lambda: int(input())

a, b = 0, 0
winners = ['x', 'jack', 'queen', 'king', 'ace']

cards = [input() for _ in range(52)]

for i in range(52):
  card = cards[i]
  if card not in winners:
    continue
  p = winners.index(card)
  if 52 - i - 1 < p:
    continue
  if any([x in winners for x in cards[i+1:i+1+p]]):
    continue
  print(f"Player {'B' if i % 2 else 'A'} scores {p} point(s).")
  if i % 2:
    b += p
  else:
    a += p


print(f"""Player A: {a} point(s).
Player B: {b} point(s).""")
