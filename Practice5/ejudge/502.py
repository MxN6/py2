import re

text = input()
substr = input()

if re.search(re.escape(substr), text):
    print("Yes")
else:
    print("No")