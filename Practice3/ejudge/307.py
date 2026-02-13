class Point():
    def __init__(self, x, y = None):
        if isinstance(x, str):
            x, y = list(map(int, x.split()))
        self.x = x
        self.y = y
    def show(self):
        print(f"({self.x}, {self.y})")
    def move(self, nx, ny = None):
        if isinstance(nx, str):
            nx, ny = list(map(int, nx.split()))
        self.x = nx
        self.y = ny
        print(f"({self.x}, {self.y})")
    def dist(self, ox, oy = None):
        if isinstance(ox, str):
            ox, oy = list(map(int, ox.split()))
        distance = ((self.x - ox)**2 + (self.y - oy)**2)**0.5
        print(f"{distance:.2f}")

p1 = Point(input())

p1.show()
p1.move(input())
p1.dist(input())