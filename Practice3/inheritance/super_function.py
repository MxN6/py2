class Person: # Parent
    def __init__(self, name):
        self.name = name
        print("Person constructor called")


class Employee(Person): # Child
    def __init__(self, name, salary): # overrides __init__
        super().__init__(name)   # call parent constructor
        self.salary = salary
        print("Employee constructor called")


e = Employee("Andy", 5000)

print(e.name)
print(e.salary)
