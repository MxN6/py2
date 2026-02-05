n, ns = input(), input()

ns = list(map(int, ns.split()))

for i in range(len(ns)):
    ns[i] = ns[i]**2

print(" ".join(list(map(str, ns))))