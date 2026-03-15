from ortools.sat.python import cp_model

# Let's start with a simple example problem in which there are:

# Three variables, x, y, and z, each of which can take on the values: 0, 1, or 2.
# One constraint: x != y

def simple_cpsat_program():
    model = cp_model.CpModel()

    # Create the variables
    num_vars = 3
    x = model.new_int_var(0, num_vars - 1, "x")
    y = model.new_int_var(0, num_vars - 1, "y")
    z = model.new_int_var(0, num_vars - 1, "z")

    # Create the constraint
    model.add(x != y)

    # Call the solver
    solver = cp_model.CpSolver()
    status = solver.solve(model)

    # Status	         Description
    # OPTIMAL	         An optimal feasible solution was found.
    # FEASIBLE	         A feasible solution was found, but we don't know if it's optimal.
    # INFEASIBLE	     The problem was proven infeasible.
    # MODEL_INVALID	     The given CpModelProto didn't pass the validation step. 
    # You can get a detailed error by calling ValidateCpModel(model_proto).
    # UNKNOWN	The status of the model is unknown because no solution was found 
    # (or the problem was not proven INFEASIBLE) before something caused the solver to stop,
    # such as a time limit, a memory limit, or a custom limit set by the user.

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"x = {solver.value(x)}")
        print(f"y = {solver.value(y)}")
        print(f"z = {solver.value(z)}")
    else:
        print("NO SOLUTION FOUND!")


# if __name__ == "__main__":
#     simple_cpsat_program()


# Next, we'll show how to modify the program above to find all feasible solutions.
# The main addition to the program is a solution printer a callback that you pass to
# the solver, which displays each solution as it is found.

# Add the solution printer
class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0

    # Override method, each time the solver finds a new solution, it calls this method
    def on_solution_callback(self) -> None:
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v}={self.value(v)}", end=" ")
        print()

    @property
    def solution_count(self) -> int:
        return self.__solution_count
    

def search_all_solutions_cpsat():
    model = cp_model.CpModel()

    num_vars = 3
    x = model.new_int_var(0, num_vars - 1, "x")
    y = model.new_int_var(0, num_vars - 1, "y")
    z = model.new_int_var(0, num_vars - 1, "z")

    model.add(x != y)
    # Call the solver
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinter([x, y, z])
    # Enumerate all solutions 
    solver.parameters.enumerate_all_solutions = True
    status = solver.solve(model, solution_callback=solution_printer)

    print(f"Status = {solver.status_name(status)}")
    print(f"Number of solutions found: {solution_printer.solution_count}")
    

if __name__ == "__main__":
    search_all_solutions_cpsat()