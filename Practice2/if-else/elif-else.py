# elif is basically else-if
# meaning it handles OTHER case
# but with condition.

x = 3
y = 5

if False:
    print("A")
elif x < y:
    print("B")
else:
    # else is optional IF other cases are not possible
    print("C")