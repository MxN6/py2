n = int(input())

ns = list(filter(lambda x : int(x)%2 == 0, input().split()))

print(len(ns))