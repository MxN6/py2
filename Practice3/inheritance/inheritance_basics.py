class Animal: # Parent
    def __init__(self, name):
        self.name = name

    def speak(self):
        print("Animal makes a sound")


class Dog(Animal): # Child
    def fetch(self):
        print(self.name, "is fetching!")


d = Dog("Buddy")

d.speak()   # inherited from Animal
d.fetch()   # defined in Dog