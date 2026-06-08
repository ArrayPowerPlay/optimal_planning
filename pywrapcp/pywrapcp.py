from ortools.constraint_solver import pywrapcp


solver = pywrapcp.Solver("CPSimple")
num_vals = 3
x = solver.IntVar(0, num_vals - 1, "x")
y = solver.IntVar(0, num_vals - 1, "y")
z = solver.IntVar(0, num_vals - 1, "z")

solver.Add(x != y)
print(f"Number of constraints: {solver.Constraints()}")

decision_builder = solver.Phase(
    [x, y, z], solver.CHOOSE_FIRST_UNBOUND, solver.ASSIGN_MIN_VALUE
)

count = 0
solver.NewSearch(decision_builder)
while solver.NextSolution():
    count += 1
    solution = f"Solution {count}:\n"
    for var in [x, y, z]:
        solution += f" {var.Name()} = {var.Value()}"
    print(solution)
solver.EndSearch()
print(f"Number of solution found: {count}")