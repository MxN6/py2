import math
import random

# -----------------------
# 1. Built-in Functions
# -----------------------

print("Min:", min(3, 7, 1))
print("Max:", max(3, 7, 1))
print("Absolute:", abs(-10))
print("Round:", round(3.14159, 2))
print("Power:", pow(2, 3))


# -----------------------
# 2. math Module
# -----------------------

print("Square root:", math.sqrt(16))
print("Ceil:", math.ceil(3.2))
print("Floor:", math.floor(3.8))
print("Sin(0):", math.sin(0))
print("Pi:", math.pi)
print("e:", math.e)


# -----------------------
# 3. random Module
# -----------------------

print("Random float:", random.random())
print("Random int:", random.randint(1, 10))
print("Random choice:", random.choice(["apple", "banana", "cherry"]))

items = [1, 2, 3, 4, 5]
random.shuffle(items)
print("Shuffled list:", items)

# -----------------------
# 4. random sample
# -----------------------

numbers = [1, 2, 3, 4, 5]

result = random.sample(numbers, 3)
print(result)

# -----------------------
# 5. Practice
# -----------------------

#Write a Python program to convert degree to radian.
degree = 5
radians = math.radians(degree)
print(f"deg: {degree}, rad:{radians}")

#Write a Python program to calculate the area of a trapezoid.
height = 5
upbase = 5
downbase = 6
print(height * (upbase + downbase)/2 )

#Write a Python program to calculate the area of regular polygon.
sides = 6
PolyLen = 25
print((sides * math.pow(PolyLen, 2)) / (4 * math.tan(math.pi/sides)))

#Write a Python program to calculate the area of a parallelogram.
height = 7
base = 3
print(height * base)