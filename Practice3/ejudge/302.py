n = int(input())

def isUsual(num):
    while num != 1:
        if num % 2 != 0 and num % 3 != 0 and num % 5 != 0:
            return False
        if num % 2 == 0:
            num /= 2
        if num % 3 == 0:
            num /= 3
        if num % 5 == 0:
            num /= 5
    return True

print("Yes" if isUsual(n) else "No")