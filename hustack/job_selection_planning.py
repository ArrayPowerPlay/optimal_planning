import sys


def read_input():
    lines = list(map(int, sys.stdin.read().split()))
    n = lines[0]
    # X stores pairs of (deadline, profit)
    X = []

    k = 1
    for _ in range(n):
        X.append((lines[k], lines[k + 1]))
        k += 2

    return X


def simple_solution(X):
    X.sort(key=lambda x: x[1], reverse=True)

    max_deadline = max(d for d, p in X)
    marked = [False] * (max_deadline + 1)
    total_profit = 0

    for deadline, profit in X:
        for i in range(deadline, 0, -1):
            if not marked[i]:
                marked[i] = True
                total_profit += profit
                break

    return total_profit


def disjoint_set_union(X):
    # Use Disjoint Set Union — DSU to quickly find the latest available slots
    X.sort(key=lambda x: x[1], reverse=True)

    max_deadline = max(d for d, p in X)
    parent = [i for i in range(max_deadline + 1)]

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    total_profit = 0
    for deadline, profit in X:
        t = find(deadline)
        if t > 0:
            parent[t] = find(t - 1)
            total_profit += profit
    
    return total_profit


if __name__ == "__main__":
    X = read_input()
    result = disjoint_set_union(X)
    print(result)
