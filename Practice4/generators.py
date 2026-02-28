# -----------------------
# 1. Basic Iterator Usage
# -----------------------

numbers = [1, 2, 3, 4]

iterator = iter(numbers)

print("Using iter() and next():")
print(next(iterator))
print(next(iterator))
print(next(iterator))
print(next(iterator))


# -----------------------
# 2. Loop Through Iterator
# -----------------------

print("\nLooping through iterator:")
for num in numbers:
    print(num)


# -----------------------
# 3. Create Custom Iterator
# -----------------------

class CountUpTo:
    def __init__(self, max_value):
        self.max = max_value
        self.current = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= self.max:
            value = self.current
            self.current += 1
            return value
        else:
            raise StopIteration

print("\nCustom Iterator:")
counter = CountUpTo(5)
for number in counter:
    print(number)


# -----------------------
# 4. Generator Function
# -----------------------

def square_generator(n):
    for i in range(n):
        yield i * i

print("\nGenerator Function:")
for value in square_generator(5):
    print(value)


# -----------------------
# 5. Generator Expression
# -----------------------

print("\nGenerator Expression:")
gen_expr = (x * 2 for x in range(5))
for value in gen_expr:
    print(value)