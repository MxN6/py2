n = int(input())

nmax = "e"
posmax = 0
numbers = input().split()
for i in range(n):
    if nmax == "e":
        nmax = int(numbers[i])
    elif int(numbers[i]) > nmax:
        nmax = int(numbers[i])
        posmax = i

print(posmax+1)