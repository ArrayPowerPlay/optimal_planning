import math
import random
import sys

sys.setrecursionlimit(10**7)

n = int(input())
coords = []
orders = []

for _ in range(n):
    _, x, y, o = input().split()
    coords.append(float(x), float(y))
    orders.append(int(o))

adj = [[] for _ in range(n)]
q = int(input())

for _ in range(q):
    u, v = map(int, input().split())
    adj[u].append(v)
    adj[v].append(u)

m, alpha = input().split()
m = int(m)
alpha = float(alpha)

dist = [[0] * n for _ in range(n)]
for i in range(n):
    for j in range(n):
        # math.hypot(x, y) = sqrt(x^2 + y^2)
        dist[i][j] = math.hypot(coords[i][0] - coords[j][0], coords[i][1] - coords[j][1])

total = sum(orders)
mu = total / m
LOW = (1 - alpha) * mu
HIGH = (1 + alpha) * mu

def get_components(cluster):
    """Return a list of lists of connect components in a cluster"""
    visited = set()
    comps = []

    for u in cluster:
        if u in visited:
            continue
        stack = [u]
        comp = []

        while stack:
            x = stack.pop()
            if x in visited:
                continue
            visited.add(x)
            comp.append(x)
            for v in adj[x]:
                if v in cluster and v not in visited:
                    stack.append(v)

        comps.append(comp)
    return comps


def is_connected(cluster):
    """Check if a cluster is a connected graph"""
    return len(get_components(cluster)) == 1


def cluster_cost(cluster):
    """Find the smallest compactness of a cluster"""
    best = float('inf')
    for c in cluster:
        s = 0
        for u in cluster:
            s += dist[u][c]
        best = min(best, s)
    return best


### Build without connectivity
def build_solution():
    """Build a greedy solution for initialization, only take into account HIGH constraint"""
    nodes = list(range(n))
    random.shuffle(nodes)

    clusters = [[] for _ in range(m)]
    weights = [0] * m

    # Examine each node individually and assign them to each cluster
    for u in nodes:
        best_j = -1
        best_diff = float('inf')

        for j in range(m):
            if weights[j] + orders[u] > HIGH:
                continue
            diff = abs((weights[j] + orders[u]) - mu)
            if diff < best_diff:
                best_diff = diff
                best_j = j
        
        if best_j == -1:
            return None
        
        clusters[best_j].append(u)
        weights[best_j] += orders[u]
    
    return clusters


def repair(clusters):
    """Loop for each cluster. For each unconnected cluster, keep its largest component
    and re-distribute the remaining components"""
    for j in range(m):
        comps = get_components(clusters[j])
        if len(comps) <= 1:
            continue

        # Only keep the largest connected component in the cluster, the remainings
        # are re-distributed to its neighbors
        comps.sort(key=len, reverse=True)
        main = comps[0]

        clusters[j] = main[:]

        for comp in comps[1:]:
            for u in comp:
                for k in range(m):
                    if k == j:
                        continue
                    # Find u's neighbors and assign u to its neighbor's cluster
                    if any(v in clusters[k] for v in adj[u]):
                        clusters[k].append(u)
                        break
    return clusters


def improve(clusters):
    """Move one node from a cluster to another cluster, with 2 conditions: keep connectivity
    and the movement must reduce total cost of two clusters"""
    changed = True

    while changed:
        changed = False

        for i in range(n):
            for j1 in range(m):
                if i not in clusters[j1]:
                    continue

                for j2 in range(m):
                    if j1 == j2:
                        continue

                    w1 = sum(orders[x] for x in clusters[j1])
                    w2 = sum(orders[x] for x in clusters[j2])

                    # Check HIGH, LOW condition
                    if w2 + orders[i] > HIGH or w1 - orders[i] < LOW:
                        continue
                    new1 = [x for x in clusters[j1] if x != i]
                    new2 = clusters[j2] + [i]

                    # Check connectivity
                    if not is_connected(new1) or not is_connected(new2):
                        continue
                    
                    # Check total cost of two clusters
                    old = cluster_cost(clusters[j1]) + cluster_cost(clusters[j2])
                    new = cluster_cost(new1) + cluster_cost(new2)

                    if new < old:
                        clusters[j1] = new1
                        clusters[j2] = new2
                        changed = True
                        break
                if changed:
                    break
            if changed:
                break

    return clusters


best = float('inf')

for _ in range(200):         # Multi restart
    sol = build_solution()
    if sol is None:
        continue

    # Ensure connectivity
    sol = repair(sol)
    # Improve (reduce) total costs and ensure connectivity
    sol = improve(sol)

    ok = True

    for c in sol:
        # Check connected graph constraint
        if not is_connected(c):
            ok = False
            break
        w = sum(orders[x] for x in c)
        # Check HIGH, LOW constraint
        if not (LOW <= w <= HIGH):
            ok = False
            break
    if not ok:
        continue

    val = sum(cluster_cost(c) for c in sol)
    best = min(best, val)

if best == float('inf'):
    print(-1)
else:
    print(f"{best:.2f}")



