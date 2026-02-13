class Pair():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    def add(self, op1, op2):
        self.p1 += op1
        self.p2 += op2
    def display(self):
        print(self.p1, self.p2)

nums = tuple(map(int, input().split()))

one = Pair(nums[0], nums[1])
one.add(nums[2], nums[3])
print("Result: ", end="")
one.display()