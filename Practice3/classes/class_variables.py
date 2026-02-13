# variables in class and object are called
# Properties.
# There are two type of it as you can guess
# Class and Object Properties.

class Person():
    # Class property
    alive = True
    def __init__(self, name):
        # Object property
        self.name = name

# Important notice: class do not restrict the scope of access
# Just like functions does not.

Andy = Person("Andy")
Kate = Person("Kate")

print(Andy.alive, Kate.alive)
print(Andy.name, Kate.name)

# Btw, we can create Object and class properties
# Out of thin air
Person.breathing = True
Andy.gender = "male"
Kate.loves = "Andy"

print(Andy.breathing)
print(Kate.loves)