n = int(input())

d = dict()

for i in range(n):
    dor, s = input().split()
    s = int(s)
    if dor not in d:
        d[dor] = s
    else:
        d[dor] += s

for k,v in sorted(d.items()):
    print(k, v)