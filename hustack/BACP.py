from ortools.sat.python import cp_model
import sys
import random

def solve_bacp_ortools(n, p, credits, Q, alpha, beta, lamda, gamma):
    model = cp_model.CpModel()

    # x[i, j] = course i assigned at semester j
    x = {}
    for i in range(1, n + 1):
        for j in range(1, p + 1):
            x[(i, j)] = model.new_bool_var(f'x_{i}_{j}')

    # A course can only be assigned at one semester
    for i in range(1, n + 1):
        model.add(sum(x[(i, k)] for k in range(1, p + 1)) == 1)

    for k in range(1, p + 1):
        model.add(sum(x[(i, k)] for i in range(1, n + 1)) >= alpha)
        model.add(sum(x[(i, k)] for i in range(1, n + 1)) <= beta)
        model.add(sum(credits[i][k] * x[(i, k)] for i in range(1, n + 1)) >= lamda)
        model.add(sum(credits[i][k] * x[(i, k)] for i in range(1, n + 1)) <= gamma)

    # Prerequisites condition
    for (i, j) in Q:
        semester_i = sum(x[(i, k)] * k for k in range(1, p + 1))
        semester_j = sum(x[(j, k)] * k for k in range(1, p + 1))
        model.add(semester_i < semester_j)

    solver = cp_model.CpSolver()
    status = solver.Solve()

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(1, n + 1):
            for j in range(1, p + 1):
                if solver.Value(x[(i, k)]):
                    print(f"Course {i} is assigned to semester {j}")


def read_input():
    idx = 0
    input = sys.stdin.read().split()

    n = int(input[idx]); idx += 1
    p = int(input[idx]); idx += 1
    
    credits = []
    for _ in range(n):
        credits.append(int(input[idx]))
        idx += 1

    m = int(input[idx])
    Q = []
    for _ in range(m):
        i = int(input[idx]); idx += 1
        j = int(input[idx]); idx += 1
        Q.append((i, j))

    alpha = int(input[idx]); idx += 1
    beta = int(input[idx]); idx += 1
    lamda = int(input[idx]); idx += 1
    gamma = int(input[idx]); idx += 1

    return n, p, credits, Q, alpha, beta, lamda, gamma


def solve_bacp_tabu_search(n, p, credits, Q, alpha, beta, lamda, gamma):
    # Initialize random solution
    # current_sol[c] = p => course c + 1 is assigned to semester p
    current_sol = [random.randint(1, p) for _ in range(n)]
    best_sol = list(current_sol)
    
    # Tabu list: tabu[course][semester] = k (expiration step)
    tabu_list = [[0] * (p + 1) for _ in range(n)]
    tbl_length = 10

    def get_violations(sol):
        """Count the number of violations from the current solution"""
        violation = 0
        # Violate the prerequisite condition
        for (i, j) in Q:
            if sol[i - 1] >= sol[j - 1]:
                violation += 1
        
        for k in range(1, p + 1):
            courses_count = sum(1 for s in sol if s == k)
            total_credits = sum(credits[i] for i, s in enumerate(sol) if s == k)

            # Number of courses/semester condition
            if courses_count < alpha: violation += (alpha - courses_count)
            if courses_count > beta: violation += (courses_count - beta)
            # Number of credits/semester condition
            if total_credits < lamda: violation += (lamda - total_credits)
            if total_credits > gamma: violation += (total_credits - gamma)
        return violation

    best_violation = get_violations(best_sol)

    for it in range(10000):
        if best_violation == 0: break
        best_move = None
        min_move_violation = float('inf')
        
        # Check all possible moves
        for i in range(n):
            for v in range(1, p + 1):
                if current_sol[i] == v: continue

                old_v = current_sol[i]
                current_sol[i] = v
                curr_violations = get_violations(current_sol)
                # Check aspiration 
                if tabu_list[i][v] <= it or curr_violations < best_violation:
                    if curr_violations < min_move_violation:
                        min_move_violation = curr_violations
                        best_move = (i, v)

                current_sol[i] = old_v    # Reset old state
        
        if best_move:
            i, v = best_move
            current_sol[i] = v
            tabu_list[i][v] = it + tbl_length
            if min_move_violation < best_violation:
                best_violation = min_move_violation
                best_sol = list(current_sol)
    
    return best_sol, best_violation


def main():
    n, p, credits, Q, alpha, beta, lamda, gamma = read_input()
    solve_bacp_ortools(n, p, credits, Q, alpha, beta, lamda, gamma)
    # solve_bacp_tabu_search(n, p, credits, Q, alpha, beta, lamda, gamma)