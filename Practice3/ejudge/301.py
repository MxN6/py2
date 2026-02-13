n = int(input())

while n > 0:
    digit = n % 10
    if digit % 2 != 0:
        print("Not valid")
        break
    else:
        n = n//10
else:
    print("Valid")
