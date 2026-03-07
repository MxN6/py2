import re

text = input()
pattern = input()

# Use re.escape to treat pattern literally
matches = re.findall(re.escape(pattern), text)
print(len(matches))