n = int(input())

d = dict()

for i in range(n):
    x = input()
    if x not in d:
        d[x] = i + 1

for k,v in sorted(d.items()):
    print(k, v)