import re

text = input()
pattern = input()

# Treat pattern literally
matches = re.findall(re.escape(pattern), text)
print(len(matches))