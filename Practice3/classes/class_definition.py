# OOP is mainly work with classes and objects
# Class is blueprint
# Object is object

class Car():
    speed = 120 # in kilometers
    type = "Sedan"
    engine = "Inline 4, 1.5 liters, diesel"

Cobalt = Car()
Person = Car() # as you can see
# anything can be object of class
print(Cobalt.speed)
print(Person.type)

del Person # we can delete objects
# just like anything

print(Person.speed) # error