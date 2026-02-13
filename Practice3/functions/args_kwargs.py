# *args and **kwargs are ways to unpack
# list(tuple) and dictionary respectively

def my_function(greet, *args):
  print("something", greet)
  print("Type:", type(args))
  print("First argument:", args[0])
  print("Second argument:", args[1])
  print("All arguments:", args)

my_function("Hello", "Emil", "Tobias", "Linus")

li = ["Emil", "Tobias", "Linus"]
tu = ("Emil", "Tobias", "Linus")
my_function("Hello", *li) # important!!
my_function("Hello", *tu)

def my_function(greet, **myvar):
  print("something", greet)
  print("Type:", type(myvar))
  print("Name:", myvar["name"])
  print("Age:", myvar["age"])
  print("All data:", myvar)

my_function("Hi", 
            name = "Tobias", 
            age = 30, 
            city = "Bergen")

di = {"name" : "Tobias", 
      "age" : 30, 
      "city" : "Bergen"}

my_function("Hi", **di) # important!!
