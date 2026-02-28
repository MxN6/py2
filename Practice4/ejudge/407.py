line = input()
reversa = (line[len(line) - 1 - i] for i in range(len(line)))

for i in range(len(line)):
    print(next(reversa), end="")