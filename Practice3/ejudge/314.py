n = int(input())

nums = list(map(int, input().split()))

constant = 0

operations = {
"add" : lambda x: constant + x,
"multiply" : lambda x: constant * x,
"power" : lambda x: x**constant,
"abs" : lambda x: -x if x < 0 else x,
}

nop = int(input())

for i in range(nop):
    command, *constant = input().split()
    constant = int(constant[0]) if constant else None
    
    nums = [operations[command](num) for num in nums]

print(*nums)