import sys
import random

def main():
    input_data = sys.stdin.read().split()
    if not input_data: return
    n = int(input_data[0])

    x = [-1] * (n + 1)
    conflict = [0] * (n + 1)  # number of queens per row
    diag1 = [0] * (2 * n)     # row - col + (n - 1)
    diag2 = [0] * (2 * n)     # row + col - 2

    # 1. Initialize solution (greedy with early-exist)
    for col in range(1, n + 1):
        min_conflict = 10 ** 9
        best_row = []
        
        # Random hàng bắt đầu để tránh dồn quân hậu về đầu bàn cờ
        start_row = random.randint(1, n) 
        
        for step in range(n):
            row = (start_row + step - 1) % n + 1
            
            # Inline function thay vì gọi get_score()
            sum_conflict = conflict[row] + diag1[row - col + n - 1] + diag2[row + col - 2]
            
            if sum_conflict == 0:
                best_row = [row]
                break  # Thoát sớm lập tức vì 0 là số xung đột tối thiểu
                
            if sum_conflict < min_conflict:
                min_conflict = sum_conflict
                best_row = [row]
            elif sum_conflict == min_conflict:
                best_row.append(row)

        selected_row = random.choice(best_row)
        x[col] = selected_row
        conflict[selected_row] += 1
        diag1[selected_row - col + n - 1] += 1
        diag2[selected_row + col - 2] += 1

    # 2. CẢI THIỆN SOLUTION (Min-Conflicts)
    max_steps = 5 * 10 ** 4

    for _ in range(max_steps):
        # Randomly find a conflicted column
        col = None
        for _ in range(100):
            candidate_col = random.randint(1, n)
            row = x[candidate_col]
            # Inline current_score()
            if conflict[row] + diag1[row - candidate_col + n - 1] + diag2[row + candidate_col - 2] - 3 > 0:
                col = candidate_col
                break
                
        if col is None:
            # Find all conflicted index columns
            conflicted_cols = []
            for c in range(1, n + 1):
                r = x[c]
                if conflict[r] + diag1[r - c + n - 1] + diag2[r + c - 2] - 3 > 0:
                    conflicted_cols.append(c)

            if not conflicted_cols:
                print(n)
                print(" ".join(str(x[i]) for i in range(1, n + 1)))
                return
            
            col = random.choice(conflicted_cols)
            
        # Rút quân hậu khỏi vị trí cũ
        r_old = x[col]
        conflict[r_old] -= 1
        diag1[r_old - col + n - 1] -= 1
        diag2[r_old + col - 2] -= 1
        
        # Tìm hàng tốt nhất (Có Early-Exit tương tự khởi tạo)
        min_c = 10 ** 9
        best_rows = []
        start_row = random.randint(1, n)
        
        # Tính toán trước hằng số cho vòng lặp để Python chạy cực nhanh
        offset1 = n - 1 - col
        offset2 = col - 2

        for step in range(n):
            row_candidate = (start_row + step - 1) % n + 1
            s = conflict[row_candidate] + diag1[row_candidate + offset1] + diag2[row_candidate + offset2]
            
            if s == 0:
                best_rows = [row_candidate]
                break # Thoát sớm vì tìm được vị trí lý tưởng
                
            if s < min_c:
                min_c = s
                best_rows = [row_candidate]
            elif s == min_c:
                best_rows.append(row_candidate)
        
        # Assign vị trí tối ưu
        optimal_row = random.choice(best_rows)
        x[col] = optimal_row
        conflict[optimal_row] += 1
        diag1[optimal_row - col + n - 1] += 1
        diag2[optimal_row + col - 2] += 1

    print(-1)

if __name__ == "__main__":
    main()