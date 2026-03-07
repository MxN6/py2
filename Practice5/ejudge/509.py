import re

s = input()

# \b: word boundary, \w{3}: exactly 3 word characters
words = re.findall(r'\b\w{3}\b', s)
print(len(words))