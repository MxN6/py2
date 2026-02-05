n = int(input())

ns = list(map(int, input().split()))

ns.sort(reverse=True)

print(" ".join(list(map(str, ns))))