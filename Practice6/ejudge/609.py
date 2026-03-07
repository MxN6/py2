n = int(input())

keys = input().split()
values = input().split()

book = dict(zip(keys, values))
print(book.get(input(), "Not found"))