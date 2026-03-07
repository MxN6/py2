import re

# ------------------------------
# 1. re.search() – find first match
# ------------------------------
text = "Contact: john@example.com for info"
match = re.search(r'\S+@\S+\.\S+', text)
if match:
    print("re.search():", match.group())  # Output: john@example.com

# ------------------------------
# 2. re.findall() – find all matches
# ------------------------------
text = "My numbers are 12, 345, 7, 89"
matches = re.findall(r'\d{2,}', text)  # sequences of 2 or more digits
print("re.findall():", matches)  # Output: ['12', '345', '89']

# ------------------------------
# 3. re.split() – split by regex pattern
# ------------------------------
text = "apple,orange;banana|grape"
parts = re.split(r'[,;|]+', text)
print("re.split():", parts)  # Output: ['apple', 'orange', 'banana', 'grape']

# ------------------------------
# 4. re.sub() – replace pattern
# ------------------------------
text = "Price: $5, Tax: $2"
new_text = re.sub(r'\$', '', text)  # remove all $ signs
print("re.sub():", new_text)  # Output: Price: 5, Tax: 2

# ------------------------------
# 5. Metacharacters
# ------------------------------
# ^ start, $ end
text = "Hello1"
if re.match(r'^[A-Za-z].*\d$', text):
    print("Starts with letter, ends with digit: Yes")

# Alternation |
text = "I have a dog"
if re.search(r'cat|dog', text):
    print("Contains 'cat' or 'dog': Yes")

# Character classes []
text = "Hello World"
uppercase_letters = re.findall(r'[A-Z]', text)
print("Uppercase letters:", uppercase_letters)  # ['H', 'W']

# ------------------------------
# 6. Special sequences
# ------------------------------
text = "User123 data45"
print("Digits:", re.findall(r'\d', text))   # ['1','2','3','4','5']
print("Words:", re.findall(r'\w+', text))   # ['User123', 'data45']
print("Spaces:", re.findall(r'\s', text))   # [' ']

# Word boundaries \b
text = "cat catalog scat"
words = re.findall(r'\bcat\b', text)
print("Exact word 'cat':", words)  # ['cat']

# ------------------------------
# 7. Quantifiers
# ------------------------------
text = "aa ab a"
print("a*:", re.findall(r'a*', text))  # ['aa', '', 'a', '', 'a', '']
print("a+:", re.findall(r'a+', text))  # ['aa', 'a', 'a']
print("a?:", re.findall(r'a?', text))  # ['a', 'a', '', 'a', '', 'a', '']

# {n}, {n,}, {n,m}
text = "12 123 1234 1"
print("{2} digits:", re.findall(r'\d{2}', text))    # ['12', '12', '34']
print("{2,} digits:", re.findall(r'\d{2,}', text))  # ['12', '123', '1234']
print("{2,3} digits:", re.findall(r'\d{2,3}', text))# ['12', '123', '123']

# ------------------------------
# 8. re.compile()
# ------------------------------
text = "Hello 123 World 456"
pattern = re.compile(r'\d+')
matches = pattern.findall(text)
print("Compiled pattern digits:", matches)  # ['123', '456']

# ------------------------------
# 9. Flags
# ------------------------------
# re.IGNORECASE
text = "hello Hello HeLLo"
matches = re.findall(r'hello', text, flags=re.IGNORECASE)
print("Ignore case:", matches)  # ['hello', 'Hello', 'HeLLo']

# re.MULTILINE
text = "Start\nEnd\nStart"
matches = re.findall(r'^Start', text, flags=re.MULTILINE)
print("Multiline start match:", matches)  # ['Start', 'Start']

# ------------------------------
# 10. Combining concepts
# ------------------------------
# Extract name and age
text = "Name: Alice, Age: 25"
match = re.match(r'Name: (.+), Age: (\d+)', text)
if match:
    name, age = match.groups()
    print("Name and Age:", name, age)  # Alice 25

# Double every digit
text = "123abc"
result = re.sub(r'\d', lambda m: m.group()*2, text)
print("Double digits:", result)  # 112233abc