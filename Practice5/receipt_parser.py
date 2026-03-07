import re

with open("raw.txt", "r", encoding="utf-8") as file:
    content = file.read()  # reads the entire file into a string

first = re.findall('ab*', content)
print("1:", first if first else None)

second = re.search('ab{2,3}', content)
print("2:", second.group() if second else None)

third = re.search('[a-z]+_[a-z]+', content)
print("3:", third.group() if third else None)

fourth = re.findall('[A-Z][a-z]+', content)
print("4:", fourth if fourth else None)

fifth = re.search('a.*?b', content)
print("5:", fifth if fifth else None)

sixth = re.sub(r'[ .,]', ':', content)
print("6:", sixth)

def snake_to_camel(s):
    parts = s.split('_')
    return parts[0] + ''.join(p.capitalize() for p in parts[1:])

seventh = re.sub(r'\b[a-z]+(?:_[a-z]+)+\b', lambda m: snake_to_camel(m.group()), content)
print("7:", seventh)

eighth = re.split(r'(?=[A-Z])', content)
print("8:", eighth)

nineth = re.sub(r'(?<!^)(?=[A-Z])', ' ', content)
print("9:", nineth)

def camel_to_snake(s):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()

tenth = re.sub(r'\b[a-z]+[A-Z][a-zA-Z]*\b', lambda m: camel_to_snake(m.group()), content)
print("10:", tenth)