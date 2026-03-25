with open("files.txt", "x") as fe: # we create using x
    fe.write("sometimes The person")

with open("files.txt", "w") as f: # we overwrite using w
    f.write("Something something")

with open("files.txt", "a") as d: # and append using a
    d.write("Appended")

with open("files.txt", "rt") as fef: # and read
    foo = fef.read()

print(foo)