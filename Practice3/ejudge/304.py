class StringHandler():
    def __init__(self):
        self.string = "default string"
    def getString(self):
        self.string = input()
    def printString(self):
        print(self.string.upper())

sh = StringHandler()

sh.getString()
sh.printString()