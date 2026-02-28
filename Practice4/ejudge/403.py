n = int(input())

twelves = (i for i in range(0, n + 1) if i % 12 == 0)

for i in range(n // 12 + 1):
    print(next(twelves), end=" ")