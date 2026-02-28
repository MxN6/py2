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