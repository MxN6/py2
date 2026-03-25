# Task: List files with their order number
files = ["data.csv", "report.pdf", "image.png"]

print("File indexing:")
for index, filename in enumerate(files, start=1):
    print(f"{index}. {filename}")

# Task: Pair filenames with their sizes
filenames = ["data.csv", "report.pdf", "image.png"]
sizes = ["2MB", "15MB", "1.2MB"]

print("\nFile details:")
for name, size in zip(filenames, sizes):
    print(f"File: {name} | Size: {size}")

# Pro Tip: You can turn a zip object directly into a dictionary!
file_dict = dict(zip(filenames, sizes))
print("\nDictionary from zip:", file_dict)

names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for i, (name, score) in enumerate(zip(names, scores), start=1):
    print(f"Rank {i}: {name} scored {score}")