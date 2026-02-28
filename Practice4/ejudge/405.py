def countdown(sec):
    for i in range(sec + 1):
        yield sec - i

n = int(input())

print(*countdown(n), sep="\n")