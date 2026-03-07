n = input()

p1 = list(map(int, input().split()))
p2 = list(map(int, input().split()))

x = zip(p1, p2)

total = 0
for e1, e2 in x:
    total += e1 * e2
print(total)