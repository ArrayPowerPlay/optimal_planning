import sys
from ortools.sat.python import cp_model

def main():
    m, n = map(int, sys.stdin.readline().split())
    
    # teach_course[i][j] = 1 -> teacher i can teach course j
    teach_course = [[0] * n for _ in range(m)]
    for i in range(m):
        lst = list(map(int, sys.stdin.readline().split()))
        for j in lst[1:]:
            teach_course[i][j - 1] = 1

    k = int(sys.stdin.readline())
    # conflict[i][j] = 1 -> course i and j cannot be taught by the same teacher
    conflict = [[0] * n for _ in range(n)]
    for i in range(k):
        a, b = map(int, sys.stdin.readline().split())
        conflict[a - 1][b - 1] = 1
        conflict[b - 1][a - 1] = 1

    model = cp_model.CpModel()
    # x[i][j] = 1 -> assign course i to teacher j
    x = []
    for i in range(n):
        row = [model.new_bool_var(f"x[{i}][{j}]") for j in range(m)]
        x.append(row)

    y = model.new_int_var(0, n, "y")

    # teach_course[i][j] = 0 -> x[j][i] = 0
    for t in range(m):
        for c in range(n):
            if teach_course[t][c] == 0:
                model.add(x[c][t] == 0)

    # For every pair of classes c1 and c2 such that conflict(c1,c2) = 1, for every t = 0,…, M-1, 
    # state the constraint x[c1,t] + x[c2,t] <= 1
    for c1 in range(n):
        for c2 in range(c1 + 1, n):
            if conflict[c1][c2] == 1:
                for t in range(m):
                    model.add(x[c1][t] + x[c2][t] <= 1)
    
    # Each class can only be assigned to one teacher
    for i in range(n):
        model.add(sum(x[i][j] for j in range(m)) == 1)

    for j in range(m):
        model.add(sum(x[i][j] for i in range(n)) <= y)

    solver = cp_model.CpSolver()
    model.minimize(y)
    solver.parameters.max_time_in_seconds = 15.0
    
    status = solver.Solve(model)

    if status in (cp_model.FEASIBLE, cp_model.OPTIMAL):
        print(solver.value(y))
    else: 
        print(-1)

    
if __name__ == "__main__":
    main()