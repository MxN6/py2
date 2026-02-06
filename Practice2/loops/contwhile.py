# "continue" is basically "pass"
# but with iterations
# what is the difference?
# well "pass" does nothing
# "continue" skips

i = -5

while i < 0:
    i += 1
    print("Eye", i)
    if i % 2 == 0:
        continue
    else:
        print("i not eye")
    print("So thy is", i)

i = -5
print()

while i < 0:
    i += 1
    print("Eye", i)
    if i % 2 == 0:
        pass
    else:
        print("i not eye")
    print("So thy is", i)
