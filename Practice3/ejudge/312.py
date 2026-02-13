class Employee():
    def __init__(self, name, base_salary):
        self.name = name
        self.salary = base_salary
    def total_salary(self):
        return self.salary

class Manager(Employee):
    def __init__(self, name, base_salary, bonus_percent):
        super().__init__(name, base_salary)
        self.bonus = bonus_percent
    def total_salary(self):
        return self.salary * (1 + self.bonus/100)

class Developer(Employee):
    def __init__(self, name, base_salary, completed_projects):
        super().__init__(name, base_salary)
        self.projects = completed_projects
    def total_salary(self):
        return self.salary + self.projects * 500

class Intern(Employee):
    pass

role, name, salary, *extra = input().split()
salary = int(salary)
extra_value = int(extra[0]) if extra else None

if role == "Manager":
    Person = Manager(name, salary, extra_value)
elif role == "Developer":
    Person = Developer(name, salary, extra_value)
elif role == "Intern":
    Person = Intern(name, salary)

print(f"Name: {Person.name}, Total: {Person.total_salary():.2f}")