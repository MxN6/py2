n = int(input())

ins = list(map(int, input().split()))
ns = set()

for i in ins:
    if i in ns:
        print("NO")
    else:
        print("YES")
        ns.add(i)