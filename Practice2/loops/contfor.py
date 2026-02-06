# "continue" in "for" does not differ
# from continue in "while"

for i in range(1,10):
    print(i, end=" is ")
    if i % 2 == 1:
        print("nothing")
        continue
    print(i)