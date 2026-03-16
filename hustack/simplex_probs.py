import sys
from ortools.linear_solver import pywraplp

def main():
    line1 = sys.stdin.readline().split()
    n, m = map(int, line1)

    data = {}
    # Coefficients of objective function
    line2 = sys.stdin.readline().split()
    data["obj_coeffs"] = list(map(int, line2))

    # Coefficients of matrix A
    data["constraint_coeffs"] = []
    for i in range(m):
        row = list(map(float, sys.stdin.readline().split()))
        data["constraint_coeffs"].append(row)

    # Coefficients of bounds
    data["bounds"] = list(map(float, sys.stdin.readline().split()))

    solver = pywraplp.Solver.CreateSolver("GLOP")
    infinity = solver.infinity()
    x = [solver.NumVar(0.0, infinity, f"x[{i}]") for i in range(n)]

    for i in range(m):
        solver.Add(sum(data["constraint_coeffs"][i][j] * x[j] 
                       for j in range(n)) <= data["bounds"][i])
    
    objective = solver.Objective()
    obj = [data["obj_coeffs"][j] * x[j] for j in range(n)]
    solver.Maximize(sum(obj))
    
    status = solver.Solve()
    if status != pywraplp.Solver.OPTIMAL:
        print("UNBOUNDED")
    else:
        print(n)
        for i in range(n):
            print(f"{x[i].solution_value():.1f}", end=" ")


if __name__ == "__main__":
    main()