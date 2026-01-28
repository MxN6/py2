s, ss, sss, ssss = "so 'so'", 'to "to"', """
multiple line string
so 'so' "so" so "si"
""", ''' Also,
multiple line string
'''

print(s, ss, sss, ssss, sep="\n")

a = "Hello World!"

print(a[0])
# starts from 0
print(a[-1])
# and ends with -1
print(a[1:3])
# substr
print(a[2:9:2])
# steps with substr
print(a[:5])
# end declared substr
print(a[3:])
# start declared substr
print(a[::-1])
# reverse steps

# length of the string
print(len(a))

# substr presence
print("Hello" in a)

# negative presence
print("Hello" not in a)

# looping str
for x in a:
    print(x)

print ("or") # or

for x in range(len(a)):
    print(a[x])

print(s+a+" "+ss) #concat

b = 34
txti = "any data type must be converted to be used like this number" + str(b)
txt = f"""format strings are very useful because instead of repeating {'str' * 5} 
you can use them straight out {b}"""
txt2 = f"Also they have cool feature like this {35/9:.2f}. this is 35/9 with 2 decimals"

print(txti)
print(txt)
print(txt2)
#                                          H   e   l   l   o   w   o   l
print("The Escape characters are followed: H\" e\\ l\n l\t o\b w \157 \x6c")

# there is so much methods...
print(a.lower())
print(a.upper()) # intuitive ones

print(a.split())
print('@'.join(a.split())) # important ones