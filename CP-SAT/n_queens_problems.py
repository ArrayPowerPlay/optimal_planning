# In this section we will solve the N-queens problem using CP-SAT

import sys
import time
from ortools.sat.python import cp_model

class NQueensSolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, queens: list[cp_model.IntVar]):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__num_solutions = 0
        self.__queens = queens
        self.__start_time = time.time()

    def on_solution_callback(self) -> None:
        current_time = time.time()
        self.__num_solutions += 1

        print(f"Solution #{self.__num_solutions}")
        print(f"Time: {current_time - self.__start_time:.4f} s")

        num_iter = range(len(self.__queens))
        for i in num_iter:
            for j in num_iter:
                if self.value(self.__queens[j]) == i:
                    print("Q", end=" ")
                else:
                    print("-", end=" ")
            print()
        

    @property
    def solution_count(self) -> int:
        return self.__num_solutions
    

def main():
    model = cp_model.CpModel()
    board_size = 10
    # This variable will hold the row position of the queen in its respective column.
    # queens[j] = i means there is a queen in row i and column j.
    queens = [model.new_int_var(0, board_size - 1, f"x_{i}") for i in range(board_size)]

    # Create the constraints
    model.add_all_different(queens)

    # No 2 queens in the same diagonal
    model.add_all_different(queens[i] + i for i in range(board_size))
    model.add_all_different(queens[i] - i for i in range(board_size))
        

    solver = cp_model.CpSolver()
    solution_printer = NQueensSolutionPrinter(queens)
    solver.parameters.enumerate_all_solutions = True
    solver.solve(model, solution_printer)


if __name__ == "__main__":
    main()
