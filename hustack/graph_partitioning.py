from ortools.sat.python import cp_model
import sys

def read_input():
    idx = 0
    input = sys.stdin.read().split()

    n = int(input[idx]); idx += 1
    m = int(input[idx]); idx += 1

    edges = []
    for _ in range(m):
        x = int(input[idx]); idx += 1
        y = int(input[idx]); idx += 1
        w = int(input[idx]); idx += 1
        edges.append((x, y, w))

    return n, edges


def graph_partitioning_ortools(n, edges):
    model = cp_model.CpModel()

    # x[i] = 0 if x in X, x[i] = 1 if x in Y
    x = [model.new_bool_var(f'x_{i}') for i in range(n)]
    # Number of nodes in each set
    model.add(sum(x) == (n // 2))

    cut_weights = []
    for u, v, w in edges:
        # cut_edge = 1 if x[u] != x[v]
        cut_edge = model.new_bool_var(f'cut_{u}_{v}')
        model.add(x[u] != x[v]).OnlyEnforceIf(cut_edge)
        model.add(x[u] == x[v]).OnlyEnforceIf(cut_edge.Not())
        cut_weights.append(cut_edge * w)
    
    model.minimize(sum(cut_weights))

    solver = cp_model.CpSolver()
    status = solver.Solve()

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return solver.ObjectiveValue()
    else: return None


def graph_partitioning_tabu_search(n, edges):
    nodes = list(range(n))
    current_X = set(nodes[:n//2])
    current_Y = set(nodes[n//2:])
    
    def get_cut_weight(partition_X):
        weights = 0
        for u, v, w in edges:
            if (u in partition_X) != (v in partition_X):
                weights += w
        return weights

    best_X = set(current_X)
    best_weight = get_cut_weight(best_X)
    tabu_list = {}   # (node, target_set) = expiration iteration
    tbl = 10         # tabu length

    for it in range(10000):
        best_move = None
        min_move_weight = float('inf')

        for u in current_X:
            for v in current_Y:
                new_weight = get_cut_weight((current_X - {u}) | {v})

                # As we want to swap (u, v) from X to Y. We need to check if this move is not banned
                is_tabu = tabu_list.get((u, 'Y'), 0) > it or tabu_list.get((v, 'X'), 0) > it
                if not is_tabu or new_weight < best_weight:
                    if new_weight < min_move_weight:
                        min_move_weight = new_weight
                        best_move = (u, v)

        if best_move:
            u, v = best_move
            current_X.remove(u)
            current_X.add(v)
            current_Y.remove(v)
            current_Y.add(u)
            tabu_list[(u, 'X')] = it + tbl
            tabu_list[(v, 'Y')] = it + tbl
            if min_move_weight < best_weight:
                best_weight = min_move_weight
                best_X = set(current_X)

    return best_weight


def main():
    n, edges = read_input()
    res = graph_partitioning_ortools(n, edges)
    # res = graph_partitioning_tabu_search(n, edges)
    print(res)