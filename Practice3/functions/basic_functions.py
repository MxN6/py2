# The function is basically a block of commands
# that you will execute when you call

def Hello():
    print("hello world!")

# Lets log a word so we can understand the call
print("first") 
Hello()
print("second")

# functions follow same rules of naming as variables do
# so lets skip that part

# The function is very useful when repetition is needed

x = 0 
def add():
    global x
    print(f"x before: {x}")
    x += 1
    print(f"x after: {x}")

for i in range(5):
    add()

print(x)
