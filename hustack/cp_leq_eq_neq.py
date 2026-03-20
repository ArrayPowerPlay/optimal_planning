import sys
from ortools.sat.python import cp_model

def main():
    variables = {}
    model = cp_model.CpModel()

    input = sys.stdin.readline
    while True:
        line = input().strip()
        if line == "#" or not line:
            break
        lines = line.split()
        if lines[0] == "Var":
            var, min_bound, max_bound = lines[1], int(lines[2]), int(lines[3])
            variables[var] = model.new_int_var(min_bound, max_bound, var)
        else:
            a, var1, b, var2, c = int(lines[1]), lines[2], int(lines[3]), lines[4], int(lines[5])
            if lines[0] == "Eq":
                model.add(a * variables[var1] == b * variables[var2] + c)
            elif lines[0] == "Leq":
                model.add(a * variables[var1] <= b * variables[var2] + c)
            else:
                model.add(a * variables[var1] != b * variables[var2] + c)

    solver = cp_model.CpSolver()
    status = solver.solve(model)
    
    if status not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(-1)
    else:
        print(len(variables))
        for k, v in variables.items():
            print(f"{k} {solver.value(v)}")


if __name__ == "__main__":
    main()