a, b = tuple(map(int, input().split()))

aToB = (i**2 for i in range(a, b + 1))

for _ in range(b - a + 1):
    print(next(aToB))