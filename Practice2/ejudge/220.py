n = int(input())

d = dict()

for i in range(n):
    s = input().split()
    c = s[0]
    k = s[1]
    if c == "set":
        d[k] = s[2]
    elif c == "get":
        if k in d:
            print(d[k])
        else:
            print(f"KE: no key {k} found in the document")