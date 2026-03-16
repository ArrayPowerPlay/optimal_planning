# 1. Setting a time limit for the solver

# If your program takes a long time to run, we recommend setting a time limit
# for the solver, which ensures that the program will terminate in a reasonable
# length of time. The examples below illustrate how to set a limit of 10 seconds
# for the solver.

from ortools.sat.python import cp_model

def solve_with_time_limit_sample():
    model = cp_model.CpModel()
    num_vals = 3
    x = model.new_int_var(0, num_vals - 1, "x")
    y = model.new_int_var(0, num_vals - 1, "y")
    z = model.new_int_var(0, num_vals - 1, "z")
    
    model.add(x != y)
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 10.0
    status = solver.solve(model)

    if status == cp_model.OPTIMAL:
        print(f"x = {solver.value(x)}")
        print(f"y = {solver.value(y)}")
        print(f"z = {solver.value(z)}")


if __name__ == "__main__":
    solve_with_time_limit_sample()


# 2. Stopping a search after a specified number of solutions
# As an alternative to setting a time limit, you can make the solver terminate after it 
# finds a specified number of solutions. The examples below illustrate how to stop the 
# search after five solutions.

class VarArraySolutionPrinterWithLimit(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables: list[cp_model.IntVar], limit):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__solution_limit = limit

    def on_solution_callback(self):
        self.__solution_count += 1
        for v in self.__variables:
            print(f"{v}={self.value(v)}", end=" ")
        print()
        
        if self.__solution_count >= self.__solution_limit:
            print(f"Stop search after {self.__solution_count} solutions")
            self.stop_search()

    @property
    def solution_count(self) -> int:
        return self.__solution_count
    

def stop_after_n_solutions():
    model = cp_model.CpModel()
    # Creates the variables.
    num_vals = 3
    x = model.new_int_var(0, num_vals - 1, "x")
    y = model.new_int_var(0, num_vals - 1, "y")
    z = model.new_int_var(0, num_vals - 1, "z")

    # Create a solver and solve.
    solver = cp_model.CpSolver()
    solution_printer = VarArraySolutionPrinterWithLimit([x, y, z], 5)
    # Enumerate all solutions.
    solver.parameters.enumerate_all_solutions = True
    # Solve.
    status = solver.solve(model, solution_printer)
    print(f"Status = {solver.status_name(status)}")
    print(f"Number of solutions found: {solution_printer.solution_count}")
    assert solution_printer.solution_count == 5


if __name__ == "__main__":
    stop_after_n_solutions()
