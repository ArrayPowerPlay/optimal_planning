import sys

sys.setrecursionlimit(1500)

def solve():
    line = sys.stdin.readline().split()
    n, Q = map(int, line)

    dist = []
    for _ in range(2 * n + 1):
        dist.append(list(map(int, sys.stdin.readline().split())))
    
    visited = [False] * (2 * n + 1)
    x = [0] * (2 * n + 1)
    f_best = float('inf')
    f = 0
    load = 0
    c_min = float('inf')

    for i in range(2 * n + 1):
        for j in range(2 * n + 1):
            if i != j:
                c_min = min(c_min, dist[i][j])
    
    def check(v):
        if visited[v]:
            return False
        if v > n:
            if not visited[v - n]:
                return False
        if v <= n:
            if load + 1 > Q:
                return False
        return True

    def Try(k):
        nonlocal load, f, f_best

        for v in range(1, 2 * n + 1):
            if not check(v):
                continue
            x[k] = v
            visited[v] = True
            if v <= n: load += 1
            else: load -= 1
            f += dist[x[k - 1]][x[k]]

            if k == 2 * n:
                f_best = min(f_best, f + dist[x[k]][x[0]])
            else:
                if f + c_min * (2 * n - k + 1) < f_best:
                    Try(k + 1)
            
            visited[v] = False
            if v <= n: load -= 1
            else: load += 1
            f -= dist[x[k - 1]][x[k]]

    Try(1)
    sys.stdout.write(f"{f_best}\n")

if __name__ == "__main__":
    solve()
