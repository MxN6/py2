def evens(n):
    for i in range(0, n + 1, 2):
        yield i

n = int(input())
ev = evens(n)

for i in range(n//2):
    print(next(ev), end = ",")

print(next(ev))