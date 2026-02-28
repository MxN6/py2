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

# -----------------------
# 6. Practice
# -----------------------

# Create a generator that generates the squares of numbers up to some number N.
N = 6
generatingSquares = (x**2 for x in range(1, N+1))
for val in generatingSquares:
    print(val)

#Write a program using generator to print the even numbers between 0 and n in comma separated form where n is input from console.
n = int(input())

def evens(n):
    for i in range(n):
        if i % 2 == 0:
            yield i

iterating = evens(n)
for i in range(n//2):
    print(next(iterating))
    

#Define a function with a generator which can iterate the numbers, which are divisible by 3 and 4, between a given range 0 and n.
By3and4 = (x for x in range(n) if x % 3 == 0 and x % 4 == 0)

for el in By3and4:
    print(el)

#Implement a generator called squares to yield the square of all numbers from (a) to (b). Test it with a "for" loop and print each of the yielded values.

a, b = 5, 8
squares = (x ** 2 for x in range(a, b+1))
for _ in range(b - a + 1):
    print(next(squares))

#Implement a generator that returns all numbers from (n) down to 0.

def reversal(n):
    for i in range(n, -1, -1):
        yield i

red = reversal(n)
for i in range(n + 1):
    print(next(red))