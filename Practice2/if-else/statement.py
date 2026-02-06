# The "if" is simple
# It is essentially a condition

if True: # statement
    print("A") # command (command block)

# if condition fails it does not execute a block

if False:
    print("B") # Do not forget about indentation!

# Since the condition is boolean, we can use anything that outputs a boolean
# lets get complex, take a class with length 0

class someclass():
    def __len__(self):
        return 0

ojb = someclass()

if ojb: # worth to notice, anything in statement automatically turns into boolean
    print("C")


x = 1
y = 3

if y >= x:
    print("LISTEN Y IS MORE THAN X")