# so if we have a statement, that runs only in specific case
# we need something that handles all other cases.
# We use "else" for this

if False:
    print("A")
else:
    # worth to notice: else runs if the statement above does not
    # execute its block, meaning it handles ALL OTHER POSSIBLE cases
    print("B")
