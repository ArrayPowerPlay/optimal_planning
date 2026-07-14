# Given an undirected graph G = (V,E). Find the minimum number of colors to color all the
# nodes of the graph (2 adjacent nodes must have different colors)
    

# Ý tưởng: Ta cần tìm k là số màu nhỏ nhất để tô, ta xét k lần lượt từ 1 đến n rồi backtrack theo k
# Ta xét điều kiện không có 2 node nào có màu trùng nhau bằng cách xây dựng ma trận kề
def is_safe(node, c, color, graph):
    # Try if we can use color 'c' to color node 'node'
    for neighbor in graph[node]:
        if color[neighbor] == c:
            return False
    return True


def backtrack(node, n, k, color, graph):
    # Try to color graph sequentially from node 'node' to node n - 1
    if node == n:
        return True     # Colored all nodes with all different colors
    
    for c in range(1, k + 1):
        if is_safe(node, c, color, graph):
            color[node] = c
            if backtrack(node + 1, n, k, color, graph):
                return True
            color[node] = 0    # Backtrack
    
    return False


def min_graph_coloring_backtrack(n, edges):
    graph = [[] for _ in range(n)]  # Xây dựng ma trận kề
    for u, v in edges:
        u -= 1
        v -= 1
        graph[u].append(v)
        graph[v].append(u)

    for k in range(1, n + 1):
        color = [0] * n    # 0 = marked as not colored yet
        # Test if we can color the graph with k colors
        if backtrack(0, n, k, color, graph):
            return k
        
    return n
    

n, m = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(m)]
print(min_graph_coloring_backtrack(n, edges))