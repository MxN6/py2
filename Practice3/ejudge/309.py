class Circle():
    def __init__(self, rad):
        self.r = rad
    def area(self):
        return 3.14159 * self.r ** 2

shenber = Circle(int(input()))

print(f"{shenber.area():.2f}")