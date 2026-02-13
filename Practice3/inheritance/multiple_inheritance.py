class Flyer:
    def fly(self):
        print("Flying...")


class Swimmer:
    def swim(self):
        print("Swimming...")


class Duck(Flyer, Swimmer):
    def speak(self):
        print("Quack!")


d = Duck()

d.fly()
d.swim()
d.speak()
# Yeah