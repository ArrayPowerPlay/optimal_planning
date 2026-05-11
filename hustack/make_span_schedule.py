import sys
from collections import deque


def main():
    lines = list(map(int, sys.stdin.read().split()))
    n, m = lines[0], lines[1]
    d = lines[2: 2 + n]

    Q = []
    k = 2 + n
    for _ in range(m):
        i, j = lines[k], lines[k + 1]
        k += 2
        Q.append((i, j))

    # Adjacent matrix
    adj = [[] for _ in range(n)]
    # inDegree[v] = number of incoming nodes that point to node v
    inDegree = [0 for _ in range(n)]
    # Use for building topological list
    q = deque()
    # Topological list
    L = []

    for (i, j) in Q:
        i -= 1
        j -= 1
        adj[i].append(j)
        inDegree[j] += 1

    for i, in_degree in enumerate(inDegree):
        if in_degree == 0:
            q.append(i)

    while q:
        u = q.popleft()
        L.append(u)
        for v in adj[u]:
            inDegree[v] -= 1
            if inDegree[v] == 0:
                q.append(v)

    F = [0 for _ in range(n)]
    # Earliest time to finish all tasks
    makeSpan = 0

    for t in L:
        if F[t] + d[t] > makeSpan:
            makeSpan = F[t] + d[t]
        for x in adj[t]:
            F[x] = max(F[x], F[t] + d[t])

    return makeSpan


if __name__ == "__main__":
    result = main()
    print(result)