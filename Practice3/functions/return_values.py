# return values are the values
# that are returned from function
# basically, the whole function gives some variable value
# for example:

def takeMeHome():
    return "To The place where I belong"

print(takeMeHome())
print(takeMeHome) # notice from output that
# brackets are essential to execute command

# more example
def some5():
    return 5

x = some5()
print(x)

# if we leave no return
# then we get None

def no():
    pass

print(no())

# if we have arguments we can return them (including lists, dicts etc.)

def a(x):
    return x

y = 9
print(y)
y = a(3)
print(y)