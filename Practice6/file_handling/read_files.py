foo = open("demofile.txt")
print(foo.read()) # whole file
foo.seek(0) # return to index 0
print(foo.read(2)) # how many to read
print(foo.readline()) # one line
print(foo.readline(3)) # Also how many to read

# However just open() is dangerous and memory inefficient
# we have to close everytime we open it
foo.close()

# But it is solvable using 'with' keyword!
with open("demofile.txt", "r") as f:
    fee = f.read()
    print(fee)