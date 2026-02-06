# "for" is iteration based loop
# it knows how long to run

basket = ["orange", "apple", "potato"]
vegetables = ["potato"]

for item in basket:
    print(f"so I see {item} in a basket")
    if item in vegetables:
        print("Oh no there is a vegetable in basket!")


# however if we want a sequence
# it would be impractical to write
sequence = [1, 4, 7, 10]

# so instead we use
sequence = range(1, 11, 3) # 1 start 10 end +3 for each item

# and we can use it in for
for i in sequence:
    print(i, end=" > ")

print() # (gap for better output)

# or use range directly
for i in range(1, 4):
    print(i, end=" before ")