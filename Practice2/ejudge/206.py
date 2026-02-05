n = int(input())

nmax = "e"
for i in input().split():
    if nmax == "e":
        nmax = int(i)
    elif int(i) > nmax:
        nmax = int(i)

print(nmax)