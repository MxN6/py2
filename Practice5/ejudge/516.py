import re

s = input()

match = re.match(r'Name: (.+), Age: (.+)', s)
if match:
    name, age = match.groups()
    print(f"{name} {age}")