n = int(input())

freq = dict()

for i in range(n):
    x = input()
    freq[x] = freq.get(i, 0) + 1

print(len(freq.keys()))