import sys
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

def read_input():
    lines = sys.stdin.read().split()
    n, Q = map(int, lines[:2])
    
    k = 2
    c = [[0 for i in range(2 * n + 1)] for j in range(2 * n + 1)]
    for i in range(2 * n + 1):
        for j in range(2 * n + 1):
            c[i][j] = int(lines[k])
            k += 1

    return n, Q, c


def solve(n, Q, c):
    num_nodes = 2 * n + 1
    depot = 0

    manager = pywrapcp.RoutingIndexManager(
        num_nodes,
        1,           # 1 vehicle
        depot
    )

    routing = pywrapcp.RoutingModel(manager)

    # Cost function
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return c[from_node][to_node]
    
    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Distance dimension
    # Use the same constraint for all vehicles
    routing.AddDimension(
        transit_callback_index,
        0,          # Slack
        1000000,    # Maximum distance that the vehicle can travel   
        True,
        "Distance"
    )
    distance_dimension = routing.GetDimensionOrDie("Distance")

    # Capacity constraint
    demands = [0] * (2 * n + 1)
    for i in range(1, n + 1):
        demands[i] = 1
        demands[i + n] = -1

    def demand_callback(from_index):
        node = manager.IndexToNode(from_index)
        return demands[node]
    
    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,           # slack
        [Q],         # Capacity of vehicle
        True,        # True if vehicle starts from depot with quantity of goods = 0
        "Capacity"
    )

    # Pickup and delivery constraint
    for i in range(1, n + 1):
        pickup = manager.NodeToIndex(i)
        delivery = manager.NodeToIndex(i + n)

        # Constraint: pickup at i => delivery at i + n
        routing.AddPickupAndDelivery(pickup, delivery)
        
        # Constraint: One vehicle must be responsible for both the pickup and delivery points
        routing.solver().Add(
            routing.VehicleVar(pickup) == routing.VehicleVar(delivery)
        )

        routing.solver().Add(
            distance_dimension.CumulVar(pickup) < distance_dimension.CumulVar(delivery)
        )

    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PARALLEL_CHEAPEST_INSERTION
    )

    solution = routing.SolveWithParameters(params)

    if not solution:
        return None
    
    index = routing.Start(0)    # First index in the first vehicle's route
    route = []

    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        if node != 0:
            route.append(node)
        index = solution.Value(routing.NextVar(index))

    return " ".join(map(str, route))


def main():
    n, Q, c = read_input()
    print(n)
    route = solve(n, Q, c)
    print(route)


if __name__ == "__main__":
    main()