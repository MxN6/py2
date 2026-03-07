import re

text = input()
pattern = input()
replacement = input()

# re.escape to treat pattern literally
result = re.sub(re.escape(pattern), replacement, text)
print(result)