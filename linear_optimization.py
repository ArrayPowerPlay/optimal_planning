# Initialize OR-tools library
from ortools.init.python import init
# Import the linear solver
from ortools.linear_solver import pywraplp

def main():
    print("Google OR tools version:", init.OrToolsVersion.version_string())

    # Declare the solver
    solver = pywraplp.Solver.CreateSolver("GLOP")  # GLOP = Google Linear Optimization Program
    if not solver:
        print("Could not create solver GLOP")
        return

    # Create the variable
    x_var = solver.NumVar(0, 1, "x")
    y_var = solver.NumVar(0, 2, "y")

    # Count defined variables
    print(f"Total of variables: {solver.NumVariables()}")

    # Define the constraint
    infinity = solver.infinity()
    solver.Add(x_var + y_var <= 2)

    # Show the number of constraint
    print(f"Number of constraints: {solver.NumConstraints()}")

    # Define the objective function
    objective = solver.Objective()
    solver.Maximize(3 * x_var + y_var)

    # Invoke the solver and display the result
    print(f"Solving with solver {solver.SolverVersion()}")
    result_status = solver.Solve()
    print(f"Status: {result_status}")
    if result_status != pywraplp.Solver.OPTIMAL:
        print("The problem does not have an optimal solution!")
        if result_status == pywraplp.Solver.FEASIBLE:
            print("A potentially suboptimal solution was found!")
        else: 
            print("The solver could not solve the problem!")
            return
        
    # Output the solution
    print("Solution:")
    print("Objective value = ", objective.Value())
    print("x =", x_var.solution_value())
    print("y =", y_var.solution_value())

    # Advanced solver information
    print("Advanced usage:")
    print(f"Problem solved in {solver.wall_time():d} miliseconds")
    print(f"Problem solved in {solver.iterations():d} iterations")


if __name__ == "__main__":
    init.CppBridge.init_logging("basic_example.py")
    cpp_flags = init.CppFlags()
    cpp_flags.stderrthreshold = True
    cpp_flags.log_prefix = False
    init.CppBridge.set_flags(cpp_flags)
    main()