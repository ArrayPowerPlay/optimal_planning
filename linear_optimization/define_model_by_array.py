# In this example we'll solve the following problem.

# Maximize 7x1 + 8x2 + 2x3 + 9x4 + 6x5 subject to the following constraints:

# 5x1 + 7x2 + 9x3 + 2x4 + x5 ≤ 250
# 18x1 + 4x2 - 9x3 + 10x4 + 12x5 ≤ 285
# 4x1 + 7x2 + 3x3 + 8x4 + 5x5 ≤ 211
# 5x1 + 13x2 + 16x3 + 3x4 - 7x5 ≤ 315
# where x1, x2, ..., x5 are non-negative integers.

from ortools.linear_solver import pywraplp

def create_data_model():
    data = {}
    data["constraint_coeffs"] = [
        [5, 7, 9, 2, 1],
        [18, 4, -9, 10, 12],
        [4, 7, 3, 8, 5],
        [5, 13, 16, 3, -7]
    ]
    data["bounds"] = [250, 285, 211, 315]
    data["obj_coeffs"] = [7, 8, 2, 9, 6]
    data["num_vars"] = 5
    data["num_constraints"] = 4

    return data


def main():
    data = create_data_model()
    solver = pywraplp.Solver.CreateSolver("SCIP")

    if not solver:
        return
    
    infinity = solver.infinity()
    x = {}
    for i in range(data["num_vars"]):
        x[i] = solver.IntVar(0, infinity, f"x[{i}]")

    print(f"Number of variables: {solver.NumVariables()}")

    # Defining the constraints
    for i in range(data["num_constraints"]):
        solver.Add(sum(data["constraint_coeffs"][i][j] * x[j] 
                       for j in range(data["num_vars"])) <= data["bounds"][i])

    objective = solver.Objective()
    obj_exp = [data["obj_coeffs"][j] * x[j] for j in range(data["num_vars"])]
    solver.Maximize(sum(obj_exp))

    print(f"Solving with {solver.SolverVersion()}")
    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        print(f"Objective value = {objective.Value()}")
        for j in range(data["num_vars"]):
            print(f"{x[j]} = {x[j].solution_value()}", end=" | ")
        print()
        print(f"Problem solved in {solver.wall_time():d} miliseconds")
        print(f"Problem solved in {solver.iterations():d} iterations")
    else:
        print("The problem does not have a optimal solution!")


if __name__ == "__main__":
    main()