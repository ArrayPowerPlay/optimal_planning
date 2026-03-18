import sys
from collections import deque


def revise(x, y, cons, domains):
    change = False
    to_remove = []

    for v1 in domains[x]:
        ok = False
        for v2 in domains[y]:
            if cons[0] == "LEQ":
                _, i, j, D = cons
                if x == i:
                    if v1 <= v2 + D:
                        ok = True
                        break
                else:
                    if v2 <= v1 + D:
                        ok = True
                        break
            else:
                _, i, j, a, b = cons
                if x == i:
                    if v1 == a * v2 + b:
                        ok = True
                        break
                else:
                    if v2 == a * v1 + b:
                        ok = True
                        break
        if not ok:
            to_remove.append(v1)
            change = True
    for v in to_remove:
        domains[x].remove(v)
    return change


def AC3(n, constraints, domains):
    Q = deque()
    # adjacents[x] = chỉ số của các ràng buộc có chứa biến x
    adjacents = [[] for _ in range(n)]
    for idx, cons in enumerate(constraints):
        if cons[0] == "LEQ":
            _, i, j, _ = cons
        else:
            _, i, j, _, _ = cons
        adjacents[i].append(idx)
        adjacents[j].append(idx)
        Q.append((idx, i, j))
        Q.append((idx, j, i))

    while Q:
        idx, x, y = Q.popleft()
        cons = constraints[idx]
        
        if revise(x, y, cons, domains):
            if len(domains[x]) == 0:
                return False
            for k in adjacents[x]:
                if k == idx:
                    continue
                cons2 = constraints[k]
                if cons2[0] == "LEQ":
                    _, a, b, _ = cons2
                else:
                    _, a, b, _, _ = cons2
                if a == x:
                    Q.append((k, b, a))
                elif b == x:
                    Q.append((k, a, b))
    return True


def main():
    input = sys.stdin.readline
    n = int(input())

    domains = []
    constraints = []
    for i in range(n):
        lst = list(map(int, input().split()))
        domains.append(set(lst))

    while True:
        line = input().strip()
        if line == '#':
            break
        parts = line.split()
        if parts[0] == "LEQ":
            _, i, j, D = parts
            constraints.append(("LEQ", int(i) - 1, int(j) - 1, int(D)))
        else:
            _, i, j, a, b = parts
            constraints.append(("EQ", int(i) - 1, int(j) - 1, int(a), int(b)))
    
    ok = AC3(n, constraints, domains)
    if not ok:
        print("FAIL")
    else:
        for i in range(n):
            vals = sorted(domains[i])
            print(len(vals), *vals)


if __name__ == "__main__":
    main()