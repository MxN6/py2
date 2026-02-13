class Shape():
    def __init__(self):
        self.areaValue = 0
    def area(self):
        return self.areaValue

class Square(Shape):
    def __init__(self, side):
        super().__init__()
        self.side = side
    def area(self):
        self.areaValue = self.side**2
        return self.areaValue

obj = Square(int(input()))

print(obj.area())