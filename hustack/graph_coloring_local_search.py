# Given an undirected graph G = (V,E). Find the minimum number of colors to color all the
# nodes of the graph (2 adjacent nodes must have different colors)

import random


def count_conflicts(n, graph, color):
    conflicts = 0
    for u in range(n):
        for v in graph[u]:
            if u < v and color[u] == color[v]:
                conflicts += 1
    return conflicts


def local_search(n, graph, k, max_steps=10000):
    color = [random.randint(0, k - 1) for _ in range(n)]

    for _ in range(max_steps):
        conflict_nodes = []

        # Find conflict nodes
        for u in range(n):
            for v in graph[u]:
                if color[u] == color[v]:
                    conflict_nodes.append(u)
                    break

        if not conflict_nodes:
            return True, color
        
        u = random.choice(conflict_nodes)
        best_color = color[u]
        best_conflict = float('inf')
        
        # Try to recolor the conflict node
        for c in range(k):
            color[u] = c
            conflict = count_conflicts(n, graph, color)

            if conflict < best_conflict:
                best_conflict = conflict
                best_color = c

        color[u] = best_color

    return False, None


def solve(n, edges):
    graph = [[] for _ in range(n)]
    for u, v in edges:
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)
    
    for k in range(1, n + 1):
        for _ in range(20):     # Restart initialization many times
            ok, _ = local_search(n, graph, k)
            if ok:
                return k
            
    return n


n, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]
print(solve(n, edges))