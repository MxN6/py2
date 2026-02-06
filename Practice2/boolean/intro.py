# booleans are either True or False.
# Anything present is True while everything empty is False

print(bool(True))
print(bool(1))
print(bool("e"))
print(bool((2)))
print(bool([3]))
print(bool({4}))

print(bool(False))
print(bool(None))
print(bool(0))
print(bool(""))
print(bool(()))
print(bool([]))
print(bool({}))

class myclass():
  def __len__(self): # __len__ of class defines bool property of the class in default
    return 0

myobj = myclass()
print(bool(myobj))


def myFunction() : # Also a function can return bools (which is very useful tbh)
  return True

print(myFunction())


x = 200

print(isinstance(x, int)) # some basic py methods return booleans

# Also there is a "pass" statement

if True:
  pass

# Its just a placeholder for a future block

# Moreover, we can nest ifs
if True:
  if bool("Truest statement ever"):
    if bool(1):
      print("GG")