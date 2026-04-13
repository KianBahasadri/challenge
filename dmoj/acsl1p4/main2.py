n, k = map(int, input().split())

# Build graph: edge from loser to winner
wins = [0] * (n + 1)
adj = [[] for _ in range(n + 1)]
for _ in range(k):
    a, b, sa, sb = map(int, input().split())
    if sa > sb:
        adj[b].append(a)
        wins[a] += 1
    else:
        adj[a].append(b)
        wins[b] += 1

# Topological elimination: repeatedly remove teams with 0 wins over remaining teams
eliminated = [False] * (n + 1)
for _ in range(n):
    for t in range(1, n + 1):
        if not eliminated[t] and wins[t] == 0:
            eliminated[t] = True
            for w in adj[t]:
                wins[w] -= 1
            break

print(sum(not eliminated[t] for t in range(1, n + 1)))
