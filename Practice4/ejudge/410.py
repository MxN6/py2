def RLG(l, rt):
    for i in range(rt):
        for el in l:
            yield el

line = input().split()
repeat = int(input())

print(*RLG(line, repeat), sep=' ')