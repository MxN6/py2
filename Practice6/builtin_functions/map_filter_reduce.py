from functools import reduce

# Sample data: A list of file sizes in Megabytes
file_sizes = [10, 50, 120, 5, 200, 15, 300]

# --- 1. filter(): Select only large files (over 100MB) ---
def is_large(n):
    return n > 100

large_files = list(filter(is_large, file_sizes))
print(f"Large files (>100MB): {large_files}")


# --- 2. map(): Convert MB to KB (Multiply by 1024) ---
def to_kb(n):
    return n * 1024

sizes_in_kb = list(map(to_kb, file_sizes))
print(f"Sizes in KB: {sizes_in_kb}") # Showing first 3


# --- 3. reduce(): Calculate the total storage used ---
def add_up(a, b):
    return a + b

total_storage = reduce(add_up, file_sizes)
print(f"Total storage used: {total_storage} MB")