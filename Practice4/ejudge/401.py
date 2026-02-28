def squares(n):
    for i in range(1, n + 1):
        yield i**2

n = int(input())
sq = squares(n)

for i in range(n):
    print(next(sq))
    
