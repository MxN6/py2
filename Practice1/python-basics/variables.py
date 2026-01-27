x = int(3) #one line - one variables
y, z = float(3), str(3) # also can use multiple vars

print(x, y, z, type(x), type(y), type(z))

s, ss = "John", 'John' # suprisingly same, s=ss

print("No number first, no spaces, no special characters except underscore for var names")
#Also, no variable that is python keyword

_myvar = my2var = 2 # Wow I never knew that I can write like that

a, b = 3, 5
s, ss = "three", "five"

print(a+b) #arithmentic
print(s+ss) #concat
print(a,b,s,ss, sep="-") #printing by separator default " " (and end="\n")

#remember x at the top?
def myfunclocal():
    x = 9 # local var
    print(x)

def myfuncglobal():
    global x # global var
    x = 3 # we can modify it btw
    print(x)

myfunclocal()
myfuncglobal()
