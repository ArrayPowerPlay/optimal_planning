import sys
import time

def main():
    start_time = time.time()
    
    # Đọc nhanh toàn bộ input
    input_data = sys.stdin.read().split()
    if not input_data:
        return
        
    n = int(input_data[0])
    
    # Chuyển ma trận về dạng 0-indexed để tính toán cho mượt
    c = []
    idx = 1
    for i in range(n):
        c.append([int(x) for x in input_data[idx:idx+n]])
        idx += n
        
    # Giới hạn thời gian để tránh TLE. Thường hệ thống cho 2.0s, set 1.8s là an toàn.
    TIME_LIMIT = 10
    
    # 1. KHỞI TẠO ĐƯỜNG ĐI (GREEDY NEAREST NEIGHBOR)
    # Thay vì random, luôn chọn thành phố gần nhất. Cách này cực nhanh và cho kết quả rất tốt.
    unvisited = set(range(1, n))
    route = [0]
    curr = 0
    while unvisited:
        # Tìm đỉnh tiếp theo có chi phí di chuyển nhỏ nhất
        next_city = min(unvisited, key=lambda city: c[curr][city])
        route.append(next_city)
        unvisited.remove(next_city)
        curr = next_city
        
    # 2. TỐI ƯU HÓA BẰNG 2-OPT (LOCAL SEARCH)
    improved = True
    while improved:
        improved = False
        # Quét mọi cặp cạnh i, j để tìm cách gỡ bỏ các đoạn chéo nhau
        for i in range(1, n - 1):
            
            # Kiểm tra thời gian, nếu sắp hết giờ thì ngắt vòng lặp để in kết quả
            if time.time() - start_time > TIME_LIMIT:
                break
                
            for j in range(i + 1, n):
                # Nếu đổi toàn bộ mảng thì lộ trình không thay đổi (chỉ đảo chiều)
                if i == 0 and j == n - 1:
                    continue
                    
                # 4 đỉnh cấu thành 2 cạnh hiện tại đang xét
                n1 = route[i - 1]
                n2 = route[i]
                n3 = route[j]
                n4 = route[(j + 1) % n]
                
                # Delta = (Chi phí 2 cạnh mới) - (Chi phí 2 cạnh cũ)
                delta = c[n1][n3] + c[n2][n4] - c[n1][n2] - c[n3][n4]
                
                # Nếu chi phí giảm, tiến hành đảo ngược đoạn đường [i...j]
                if delta < 0:
                    route[i:j+1] = reversed(route[i:j+1])
                    improved = True
                    
            if time.time() - start_time > TIME_LIMIT:
                break

    # In ra kết quả (cộng thêm 1 để chuyển từ 0-indexed về 1-indexed theo yêu cầu đề)
    print(n)
    print(" ".join(str(city + 1) for city in route))

if __name__ == "__main__":
    main()
