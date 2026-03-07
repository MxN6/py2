n = int(input())

ns = list(map(int, input().split()))

print("Yes" if all(True if el >= 0 else False for el in ns) else "No")