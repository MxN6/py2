def fibo(n):
    if n < 1: raise StopIteration
    pprev, prev, next = 0, 1, 0
    yield pprev
    yield prev
    for _ in range(n - 2):
        next = prev + pprev
        yield next
        pprev = prev
        prev = next

n = int(input())
fib = fibo(n)
for _ in range(n - 1):
    print(next(fib), end = ",")
print(next(fib) if n >= 1 else "")