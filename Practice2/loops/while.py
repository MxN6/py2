# The conditions are main key of "while" loop
# it acts as "if" but it repeates its block

i = -3
if i < 0:
    print("I am i and I am from \"if\"", i)
    i += 1

while i < 0:
    print("I am i and I am from \"while\"", i)
    i += 1

# It is important to "Falsify" your condition
# at some point of "while" iterations
# except if you want it to run endlessly

txt = "Guess the number between negative and positive infinity: "
x = input(txt)
while x != "0":
    x = input(txt)