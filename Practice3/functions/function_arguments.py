# arguments are values passed to the function
# essentially to work with it

def funcy(name):
    print("Hi "+name)

funcy("Bob!")

# "name" here is parameter
# "Bob!" is argument
# So actually we work with parameters

# Number of arguments should always be equal to the number of parameters
def ff(name, surname):
    print(f"name: {name}, surname: {surname}")

ff("Danil", "Kolbasenko")

# However, if parameter has default value (standard argument)
# It is acceptable

def fff(name, surname="Mafio"): # always declare defaults last
    print(f"Opasnyi: {name}, On {surname}")

fff("Andrey")
fff("Sergey", "Serezha")
fff("Sahsa")
fff("Eagle", "Bald")
# twice each so we nail the point

# The positions of arguments are strict
# if we do not declare which argument goes to which parameter

def animal(name, sound):
    print(f"The great {name} make sounds like {sound}")

# arguments
animal("meow", "cat") # positional
animal(sound = "meow", name = "cat") # keyword

# "can we mix?"
# Yes, first positionals and then keywords

def animal(name, sound, legs, cute):
    print(f"The great {name} make sounds like {sound}, they have {legs} legs and they are{"" if cute else " not"} cute")

animal("cat", "meow", cute = False, legs = 3)

# we can functions restrict to only-positional and only-keyword arguments

def pos(p, /):
    print(p)

def keyw(*, k):
    print(k)

pos(5) # we cant do pos(p = 5)
keyw(k = 4) # we cant do keyw(4)