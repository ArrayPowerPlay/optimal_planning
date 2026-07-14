import sys
from ortools.sat.python import cp_model
import heapq
import random


def read_input():
    input = sys.stdin.readline
    n, m = map(int, input().split())

    w = list(map(int, input().split()))
    w.insert(0, 0)
    return n, m, w


### 1. USE CP-SAT
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
    

### 2. USE GREEDY SOLUTION, THIS SOLUTION CAN BE USED FOR INITIALIZATION
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

    return n, result


### 3. USE LOCAL SEARCH WITH GREEDY INITIALIZATION
def calculate_subset_sums(n, m, w, sol):
    subset_sums = [0] * (m + 1)
    for i in range(1, n + 1):
        index_subset = sol[i]
        subset_sums[index_subset] += w[i]
    return subset_sums


def calculate_objective(subset_sums):
    return max(subset_sums[1:]) - min(subset_sums[1:])


def local_search(n, m, w, init_sol):
    current_sol = list(init_sol)
    subset_sums = calculate_subset_sums(n, m, w, current_sol)
    best_obj = calculate_objective(subset_sums)

    improved = True
    while improved:
        improved = False

        max_sum, min_sum = max(subset_sums[1:]), min(subset_sums[1:])
        maxsum_index, minsum_index = subset_sums.index(max_sum), subset_sums.index(min_sum)

        candidate_items = [i for i in range(1, n + 1) if current_sol[i] in (maxsum_index, minsum_index)]

        ### 3.1. Insert
        for choiced_item in candidate_items:
            source_set = current_sol[choiced_item]
            for target_set in range(1, m + 1):
                if target_set == source_set:
                    continue
                cand_sol = current_sol.copy()
                cand_sol[choiced_item] = target_set
                subset_sums_cand = calculate_subset_sums(n, m, w, cand_sol)
                cand_obj = calculate_objective(subset_sums_cand)

                if cand_obj < best_obj:
                    best_obj = cand_obj
                    subset_sums = subset_sums_cand
                    improved = True
                    current_sol = cand_sol
                    break
            if improved == True:
                break
        if improved == True:
            continue

        ### 3.2. Swap
        for source_item in candidate_items:
            source_set = current_sol[source_item]
            
            dist_items = [i for i in range(1, n + 1) if current_sol[i] != source_set]
            for dist_item in dist_items:
                target_set = current_sol[dist_item]
                cand_sol = current_sol.copy()
                cand_sol[source_item] = target_set
                cand_sol[dist_item] = source_set
                cand_subset_sums = calculate_subset_sums(n, m, w, cand_sol)
                cand_obj = calculate_objective(cand_subset_sums)

                if cand_obj < best_obj:
                    best_obj = cand_obj
                    current_sol = cand_sol
                    subset_sums = cand_subset_sums
                    improved = True
                    break
            if improved:
                break
    
    return current_sol, best_obj


def main():
    n, m, w = read_input()
    n, init_sol = solve_min_heap(n, m, w)
    current_sol, best_obj = local_search(n, m, w, init_sol)
    print(best_obj)
    print(*current_sol)


if __name__ == "__main__":
    main()