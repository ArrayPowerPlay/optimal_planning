import sys
from ortools.sat.python import cp_model
import heapq


def read_input():
    input = sys.stdin.readline
    n, m = map(int, input().split())

    w = list(map(int, input().split()))
    w.insert(0, 0)
    return n, m, w


def solve_cpsat(n, m, w):
    model = cp_model.CpModel()
    solver = cp_model.CpSolver()

    x = {}
    for i in range(1, m + 1): 
        for j in range(1, n + 1):
            x[(i, j)] = model.new_bool_var(f"x_{i}_{j}")

    # One item in one subset
    for j in range(1, n + 1):
        model.add(sum(x[(i, j)] for i in range(1, m + 1)) == 1)

    A = {}
    for i in range(1, m + 1):
        A[i] = sum(x[(i, j)] * w[j] for j in range(1, n + 1))

    max_sum = model.new_int_var(0, sum(w), "max_sum")
    min_sum = model.new_int_var(0, sum(w), "min_sum")

    model.add_max_equality(max_sum, [A[i] for i in range(1, m + 1)])
    model.add_min_equality(min_sum, [A[i] for i in range(1, m + 1)])
    model.minimize(max_sum - min_sum)

    status = solver.Solve(model)
    mark = [0 for _ in range(n + 1)]
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if solver.Value(x[(i, j)]) == 1:
                    mark[j] = i
                    continue

        return n, mark[1:]
    

def solve_min_heap(n, m, w):
    heap = []
    for i in range(1, m + 1):
        heapq.heappush(heap, (0, i))  # Save (total_sum, index) of a subset

    result = [0] * (n + 1)            # result[i] = subset index of item i

    items = list(range(1, n + 1))
    items.sort(key=lambda j: -w[j])

    for item in items:
        total_sum, index = heapq.heappop()
        current_sum = total_sum + w[item]
        result[item] = index
        heapq.heappush(heap, (current_sum, index))

    return n, result[1:]


def main():
    n, m, w = read_input()
    n, result = solve_min_heap(n, m, w)
    print(n)
    print(*result)


if __name__ == "__main__":
    main()