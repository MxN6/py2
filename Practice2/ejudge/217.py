n = int(input())

ns = dict()

for i in range(n):
    x = input()
    if x in ns:
        ns[x] += 1
    else:
        ns[x] = 1

bals = set()

for k,v in ns.items():
    if v == 3:
        bals.add(k)

print(len(bals))