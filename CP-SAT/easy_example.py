# Biến
# • X = {X0, X1, X2, X3, X4}
# • Miền giá trị
# • X0, X1, X2, X3, X4 thuộc {1,2,3,4,5}
# • Ràng buộc
# • C1: X2 + 3 ≠ X1
# • C2: X3 ≤ X4
# • C3: X2 + X3 = X0 + 1
# • C4: X4 ≤ 3
# • C5: X1 + X4 = 7
# • C6: X2 = 1 => X4 ≠ 2

from ortools.sat.python import cp_model
import time


class VarArraySolutionCallBack(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__num_solutions = 0
        self.start_time = time.time()
    
    def on_solution_callback(self):
        self.__num_solutions += 1
        print(f"Solution #{self.__num_solutions}")
        for v in self.__variables:
            print(f"{v} = {self.value(v)}", end="   ")
        print()

        end_time = time.time()
        print(f"Time processed: {end_time - self.start_time:.3f} s")


def main():
    model = cp_model.CpModel()
    X = [model.new_int_var(1, 5, f"X[{i}]") for i in range(5)]
    model.add(X[2] + 3 != X[1])
    model.add(X[3] <= X[4])
    model.add(X[2] + X[3] == X[0] + 1)
    model.add(X[4] <= 3)
    model.add(X[1] + X[4] == 7)
    b = model.new_bool_var("b")
    model.add(X[2] == 1).only_enforce_if(b)
    model.add(X[4] != 2).only_enforce_if(b)
    model.add(X[2] != 1).only_enforce_if(b.Not())

    solver = cp_model.CpSolver() 
    solver.parameters.search_branching = cp_model.FIXED_SEARCH

    solver.parameters.enumerate_all_solutions = True
    solution_printer = VarArraySolutionCallBack(X)
    solver.solve(model, solution_printer)
    


if __name__ == "__main__":
    main()