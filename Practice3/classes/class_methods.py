# Method is function of class
class Person:
  def __init__(self, name):
    self.name = name

  def greet(self):
    print("Hello, my name is " + self.name)

Andy = Person("Andy")

Andy.greet()

# we can add methods
# This one is actually default property
def wave(ToWhom):
  print("Hi!", ToWhom)
  
Andy.wave = wave("everyone")
Andy.wave

# default method
def dance(With):
  print("Dancing with", With)
  
Andy.dance = lambda : dance("Kate")
Andy.dance()

# Argumented method
def study(With):
  print("Studying with", With)
  
Andy.study = lambda Who: study(Who)
Andy.study("Kate")

# The methods also differ to class and object type
# we can delete it too
del Andy.study