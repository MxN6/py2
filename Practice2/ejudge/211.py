n, l, r = list(map(int, input().split()))
l -= 1
ns = list(map(int, input().split()))

mdf = ns[l:r]
del ns[l:r]
mdf = mdf[::-1]
ns = ns[:l] + mdf + ns[l:]

print(" ".join(list(map(str, ns))))