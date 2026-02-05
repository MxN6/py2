n = int(input())

ns = list(map(int, input().split()))

nmax = ns[0]
nmin = ns[0]
for i in range(len(ns)):
    if ns[i] > nmax:
        nmax = ns[i]
    if ns[i] < nmin:
        nmin = ns[i]

for i in range(len(ns)):
    if ns[i] == nmax:
        ns[i] = nmin

print(" ".join(list(map(str, ns))))