# Now I assume boolean operators mean logical ones...
# So there is 3 logical operators
# and, or and not
# they are super simple

A, C = True
B, D = False

print(A and B) # False: True and False (False dominates)
print(A and C) # True: True and True
print(A or B) # True: True or False
print(B or D) # False: False or False
print(not A) # False: not True