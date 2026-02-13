class Shape():
    def __init__(self):
        self.areaValue = 0
    def area(self):
        return self.areaValue

class Rectangle(Shape):
    def __init__(self, side1, side2 = 0):
        super().__init__()
        if type(side1) is list: # or we can do isinstance(side1, list)
            self.side1 = side1[0]
            self.side2 = side1[1]  
        else:
            self.side1 = side1
            self.side2 = side2
    def area(self):
        self.areaValue = self.side1*self.side2
        return self.areaValue

inp = list(map(int, input().split()))
obj = Rectangle(inp)

print(obj.area())