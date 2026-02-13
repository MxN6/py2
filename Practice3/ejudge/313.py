numbers = list(map(int, input().split()))

def is_prime(x):
    if x < 2:
        return False
    for i in range(2, int(x ** 0.5) + 1):
        if x % i == 0:
            return False
    return True

primes = list(filter(is_prime, numbers))

if primes:
    print(*primes)
else:
    print("No primes")