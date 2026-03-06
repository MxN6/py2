g = 0

def outer(commands):
    n = 0
    def inner():
        nonlocal n
        global g
        for scope, val in commands:
            val = int(val)
            if scope == 'global':
                g += val
            elif scope == 'nonlocal':
                n += val
            elif scope == 'local':
                x = val  # inner local only
        return n
    n = inner()
    return n

# Read input
m = int(input())
commands = [input().split() for _ in range(m)]

n_final = outer(commands)
print(g, n_final)