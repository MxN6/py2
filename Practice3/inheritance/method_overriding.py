class Bird:
    def speak(self):
        print("Bird makes a sound")


class Parrot(Bird):
    def speak(self):  # overrides parent method
        # Also called polimorphism
        print("Parrot says hello!")


b = Bird()
p = Parrot()

b.speak()
p.speak()
