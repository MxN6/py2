# init method is constructor for objects
# it can store object properties using "self" parameter
class Person:
    def __init__(self, name): # its just block of initial commands
        self.name = name
        self.greet()

    def greet(self):
        print("Created:", self.name)

Andy = Person("Andy")