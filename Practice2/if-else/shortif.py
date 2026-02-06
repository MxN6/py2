# so lets say you write this:

x = 0
if True:
    x += 1
else:
    x -= 1

# quite big huh?
# we can do it shorter:
# value "if" condition "else" value

x += 1 if True else -1

# both are same.
# use short one for shorter statements.

y = 5 if x == 3 else 6 if x == 2 else 7

# there is a three values and two ifs.
# meaning the value can be replaced with short-ifs.
# lets do monstrosity:

z = 4 if y == 2 and x == 0 else 3 if x == 1 and y == 0 else 6 if (x > 0 and y < 8) or x >= 9 else 9

# do not overuse it (like in z)