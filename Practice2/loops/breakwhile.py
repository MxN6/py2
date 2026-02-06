# "break" is exaclty what it means
# it breaks stuff
# like loops, it just makes them stop

i = -5
while i < 0:
    print("I am running!")
    i += 1
    if i == -3:
        print("Oh no I broke my ankle at i=", i, sep="")
        break
    # Oh while also runs "else" if it is present
    # after the loop.
    # however there is a special condition for it
    # it will not run if loops is broken
else:
    print("Yay I finished!")

# Okay lets heal him and let him finish

while i < 0:
    print("My ankle healed! I can run again!")
    i += 1
else:
    print("Yay I finished!")