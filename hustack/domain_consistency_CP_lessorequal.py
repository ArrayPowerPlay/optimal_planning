import sys
from collections import deque


def revise_left(i, j, D, domains):
    change = False
    to_remove = []
    for v1 in domains[i]:
        ok = False
        for v2 in domains[j]:
            if v1 <= v2 + D:
                ok = True
                break
        if not ok:
            to_remove.append(v1)
    
    for v in to_remove:
        domains[i].remove(v)
        change = True

    return change


def revise_right(i, j, D, domains):
    change = False
    to_remove = []
    for v2 in domains[j]:
        ok = False
        for v1 in domains[i]:
            if v1 <= v2 + D:
                ok = True
                break
        if not ok:
            to_remove.append(v2)
    
    for v in to_remove:
        domains[j].remove(v)
        change = True

    return change


def AC3(n, constraints, domains):
    Q = deque()
    # adjacent[x] = danh sách index các ràng buộc có chứa biến x
    adjacent = [[] for _ in range(n)]
    for idx, (i, j, D) in enumerate(constraints):
        Q.append((i, j, D, 'L'))
        Q.append((i, j, D, 'R'))
        adjacent[i].append(idx)
        adjacent[j].append(idx)

    while Q:
        i, j, D, typ = Q.popleft()
        if typ == 'L':
            changed = revise_left(i, j, D, domains)
            change_var = i
        else:
            changed = revise_right(i, j, D, domains)
            change_var = j
        if changed == True:
            if len(domains[change_var]) == 0:
                return False
            else:
                for idx in adjacent[change_var]:
                    a, b, D = constraints[idx]
                    Q.append((a, b, D, 'L'))
                    Q.append((a, b, D, 'R'))
    return True


def main():
    input = sys.stdin.readline
    n = int(input())

    domains = []
    for i in range(n):
        domain = list(map(int, input().split()))
        row = domain[1:]
        domains.append(set(row))

    m = int(input())
    constraints = []
    
    for i in range(m):
        a, b, D = map(int, input().split())
        constraints.append((a - 1, b - 1, D))

    ok = AC3(n, constraints, domains)
    if not ok:
        print("FAIL")
        return
    
    for i in range(n):
        vals = sorted(domains[i])
        print(len(vals), *vals)


if __name__ == "__main__":
    main()

