triplets = ["ZER", "ONE", "TWO", "THR", "FOU", "FIV", "SIX", "SEV", "EIG", "NIN"]

ops = ["+", "-", "*", "/"]

def triplet_split(line):
    return_list = []
    for i in range(len(line)):
        if line[i] in ops:
            return_list.append(line[:i])
            return_list.append(line[i])
            return_list.append(line[i+1:])
            break
    return return_list

def from3to1(line):
    num = ""
    for i in range(0, len(line), 3):
        if i == len(line): continue
        num += str(triplets.index(line[i:i+3]))
    return int(num)

def from1to3(num):
    num = str(num)
    line = ""
    for i in range(len(num)):
        line += triplets[int(num[i])]
    return line

n1, op, n2 = triplet_split(input())

n1, n2 = from3to1(n1), from3to1(n2)

result = n1 + n2 if op == "+" else n1 - n2 if op == "-" else n1 * n2 if op == "*" else n1 / n2

print(from1to3(int(result)))
