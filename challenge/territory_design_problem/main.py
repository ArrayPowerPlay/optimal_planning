import math
from ortools.linear_solver import pywraplp


def read_input(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    i = 0
    # Number of nodes
    n = int(lines[i])
    i += 1
    
    nodes = []
    # Store 2D position of each node
    coords = []
    # Store weights of each activity
    node_weights = []

    for _ in range(n):
        parts = lines[i].split()
        i += 1
        node = int(parts[0])
        x = float(parts[1])
        y = float(parts[2])
        activities = [float(value) for value in parts[3:]]

        nodes.append(node)
        coords.append((x, y))
        node_weights.append(activities)

    num_activities = len(node_weights[0])
    
    # Convert 'weights' of input into activity major
    weights = [
        [node_weights[j][a] for j in range(n)]
        for a in range(num_activities)
    ]

    # Number of edges
    m = int(lines[i])
    i += 1
    edges = []

    for _ in range(m):
        u, v = map(int, lines[i].split())
        i += 1
        edges.append((u, v))

    final_parts = lines[i].split()
    i += 1
    p = int(final_parts[0])
    tau = [float(x) for x in final_parts[2:]]

    # Directed arcs for flow constraints
    arcs = []
    for u, v in edges:
        arcs.append((u, v))
        arcs.append((v, u))

    outgoing = {i: [] for i in range(n)}
    incoming = {i: [] for i in range(n)}

    for u, v in arcs:
        outgoing[u].append((u, v))
        incoming[v].append((u, v))

    # Euclid distance
    dist = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        xi, yi = coords[i]
        for j in range(n):
            xj, yj = coords[j]
            dist[i][j] = math.sqrt((xi - xj)**2 + (yi - yj)**2)

    data = {
        "n": n,
        "coords": coords,
        "weights": weights,
        "num_activities": num_activities,
        "edges": edges,
        "incoming": incoming,
        "outgoing": outgoing,
        "arcs": arcs,
        "dist": dist,
        "p": p,
        "tau": tau,
    }

    return data


def solve(data, time_limit):
    n = data["n"]
    p = data["p"]
    num_activities = data["num_activities"]
    V = range(n)
    A = range(num_activities)

    weights = data["weights"]
    tau = data["tau"]
    dist = data["dist"]

    arcs = data["arcs"]
    incoming = data["incoming"]
    outgoing = data["outgoing"]

    solver = pywraplp.Solver.CreateSolver("SCIP")
    solver.SetTimeLimit(time_limit * 1000)

    x = {}
    for i in V:
        for j in V:
            x[i, j] = solver.BoolVar(f"x_{i}_{j}")

    # Maximum number of nodes that a center can give flow to
    M = n - 1    
    f = {}
    for i in V:
        for u, v in arcs:
            f[i, u, v] = solver.NumVar(0.0, M, f"f_{i}_{u}_{v}")

    solver.Minimize(
        solver.Sum(
            dist[i][j] * x[i, j]
            for i in V
            for j in V
        )
    )

    ### One node can only be linked to one center
    for j in V:
        solver.Add(solver.Sum(x[i, j] for i in V) == 1)

    ### p centers constraint
    solver.Add(solver.Sum(x[i, i] for i in V) == p)

    ### Balance constraint
    for a in A:
        total_activity = sum(weights[a][j] for j in V)
        mu = total_activity / p
        lower = (1.0 - tau[a]) * mu
        upper = (1.0 + tau[a]) * mu

        for i in V:
            territory_activity = solver.Sum(
                weights[a][j] * x[i, j] for j in V
            )

            solver.Add(territory_activity >= lower * x[i, i])
            solver.Add(territory_activity <= upper * x[i, i])

    ### Connectivity constraint using flow
    for i in V:
        ### 1. Center i gives flow = number of node (# i) in territory i
        flow_out_center = solver.Sum(
            f[i, u, v] for u, v in outgoing[i]
        )
        flow_in_center = solver.Sum(
            f[i, u, v] for u, v in incoming[i]
        )
        solver.Add(
            flow_out_center - flow_in_center == solver.Sum(x[i, j] 
            for j in V if j != i)
        )

        ### 2. Each node v # i receives one flow if x[i, v] = 1
        for v in V:
            if v == i: 
                continue
            flow_in_v = solver.Sum(
                f[i, u, w] for u, w in incoming[v]
            )
            flow_out_v = solver.Sum(
                f[i, u, w] for u, w in outgoing[v]
            )
            solver.Add(flow_in_v - flow_out_v == x[i, v])

        ## 3. Flow of territory i only goes through nodes in territory i
        for u, v in arcs:
            solver.Add(f[i, u, v] <= M * x[i, u])
            solver.Add(f[i, u, v] <= M * x[i, v])

        status = solver.Solve()
        objective = solver.Objective().Value()
        return objective


if __name__ == "__main__":
    data1 = read_input("DU150-05-1.dat")
    data2 = read_input("DU150-05-2.dat")

    result1 = solve(data1, time_limit=2000)
    result2 = solve(data2, time_limit=2000)
    
    print(round(result1, 2))
    print(round(result2, 2))