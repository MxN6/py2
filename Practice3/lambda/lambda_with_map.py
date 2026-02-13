def myfunc(n):
  return lambda a : a * n

mydoubler = myfunc(2)

# to apply function (usually lambda) to every element of the list
# we can use map
# however to work with elements
# we should convert map to list
numbers = [1, 2, 3, 4, 5]
doubled = list(map(mydoubler, numbers))
doubleds = list(map(lambda x: x * 2, numbers))
print(doubled)
print(doubleds)