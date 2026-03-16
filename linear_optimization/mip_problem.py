# Maximize x + 10y subject to the following constraints:

# x + 7y ≤ 17.5
# 0 ≤ x ≤ 3.5
# 0 ≤ y
# x, y integers

from ortools.linear_solver import pywraplp

def main():
    solver = pywraplp.Solver.CreateSolver("SCIP")

    if not solver:
        print("Cannot initialize a solver")
        return

    infinity = solver.infinity()
    x = solver.IntVar(0.0, infinity, "x")
    y = solver.IntVar(0.0, infinity, "y")

    print(f"Number of variables: {solver.NumVariables()}")

    solver.Add(x + 7 * y <= 17.5)
    solver.Add(x <= 3.5)
    solver.Maximize(x + 10 * y)

    print(f"Solving with solver version: {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
        print("SOLUTION:")
        print(f"Objective value: {solver.Objective().Value()}")
        print(f"x = {x.solution_value()}")
        print(f"y = {y.solution_value()}")
    else:
        print("The problem does not have a feasible solution!")
    
    print("Advanced usage:")
    print(f"Problem solved in {solver.wall_time():d} miliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")


if __name__ == "__main__":
    main()