import json
import sys

def resolve_query(data, query):
    current = data
    i = 0
    n = len(query)

    while i < n:
        # Parse key name
        key = ""
        while i < n and query[i] not in ".[":
            key += query[i]
            i += 1

        if key:
            if not isinstance(current, dict) or key not in current:
                return "NOT_FOUND"
            current = current[key]

        # Parse any number of [index]
        while i < n and query[i] == '[':
            i += 1
            idx_str = ""
            while i < n and query[i] != ']':
                idx_str += query[i]
                i += 1
            i += 1  # skip ']'

            if not isinstance(current, list):
                return "NOT_FOUND"

            try:
                idx = int(idx_str)
            except:
                return "NOT_FOUND"

            if idx < 0 or idx >= len(current):
                return "NOT_FOUND"

            current = current[idx]

        if i < n and query[i] == '.':
            i += 1

    return current


# Read input
data = json.loads(input())
q = int(input())

for _ in range(q):
    query = input().strip()
    result = resolve_query(data, query)

    if result == "NOT_FOUND":
        print("NOT_FOUND")
    else:
        print(json.dumps(result, separators=(',', ':')))