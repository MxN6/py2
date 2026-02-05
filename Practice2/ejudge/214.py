n = int(input())
ns = list(map(int, input().split()))

freq = dict()

for i in ns:
    freq[i] = freq.get(i, 0) + 1

mkey = ns[0]
fmax = freq[mkey]
for k, v in freq.items():
    if v > fmax:
        fmax = v
        mkey = k
    elif v == fmax:
        mkey = mkey if mkey < k else k

print(mkey)