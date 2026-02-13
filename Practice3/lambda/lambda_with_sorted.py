# we can also sort
# the return value in "key" parameter of "sorted"
# is essential to weight out element
words = ["apple", "pie", "banana", "cherry"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)

unsorted_numbers = [3,7,1,9,7,6]
sorted_numbers = sorted(unsorted_numbers, key = lambda x: x)
print(sorted_numbers)