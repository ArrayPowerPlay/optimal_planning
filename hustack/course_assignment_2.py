import sys
from ortools.sat.python import cp_model


class VarArraySolutionPrinter(cp_model.CpSolverSolutionCallback):
    def __init__(self, X, N, P):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.X = X
        self.__num_solutions = 0
        self.P = P
        self.N = N

    def on_solution_callback(self) -> None:
        self.__num_solutions += 1
        semester = [-1] * self.N
        print(f"Solution #{self.__num_solutions}")

        for i in range(self.N):
            for j in range(self.P):
                if self.value(self.X[i][j]) == 1:
                    semester[i] = j + 1
                    break
        
        for i, se in enumerate(semester):
            print(f"Semester of course {i + 1} is: {semester[i]}")

    @property
    def solution_count(self):
        return self.__num_solutions


def main():
    N, P = map(int, sys.stdin.readline().split())
    c = list(map(int, sys.stdin.readline().split()))
    k = int(sys.stdin.readline())
    L = []

    for i in range(k):
        a, b = map(int, sys.stdin.readline().split())
        L.append([a - 1, b - 1])

    alpha, beta, lamda, gamma = map(int, sys.stdin.readline().split())

    model = cp_model.CpModel()
    X = [[model.new_bool_var(f"X[{i}][{j}]") for j in range(P)] for i in range(N)]

    # Mỗi môn chỉ được phân vào 1 học kỳ
    for i in range(N):
        model.add(sum(X[i][j] for j in range(P)) == 1)
    
    # Các ràng buộc trong mỗi học kỳ
    for j in range(P):
        model.add(sum(X[i][j] for i in range(N)) <= beta)
        model.add(sum(X[i][j] for i in range(N)) >= alpha)
        model.add(sum(X[i][j] * c[i] for i in range(N)) >= lamda)
        model.add(sum(X[i][j] * c[i] for i in range(N)) <= gamma)

    # semester[i] = kỳ học của môn i
    semester = [model.new_int_var(0, P - 1, f"semester[{i}]") for i in range(N)]
    for i in range(N):
        model.add(semester[i] == sum(X[i][j] * j for j in range(P)))

    for _ in L:
        i, j = _
        model.add(semester[i] < semester[j])
    
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solution_printer = VarArraySolutionPrinter(X, N, P)
    status = solver.solve(model, solution_printer)

    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print(f"Total solutions: {solution_printer.solution_count}")
    else:
        print("The problem has no solutions")


if __name__ == "__main__":
    main()