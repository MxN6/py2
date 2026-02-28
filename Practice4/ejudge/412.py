import json
import sys

def deep_diff(obj1, obj2, path=""):
    diffs = []

    keys = set(obj1.keys()) | set(obj2.keys())

    for key in keys:
        new_path = f"{path}.{key}" if path else key

        if key not in obj1:
            new_val = json.dumps(obj2[key], separators=(',', ':'))
            diffs.append(f"{new_path} : <missing> -> {new_val}")

        elif key not in obj2:
            old_val = json.dumps(obj1[key], separators=(',', ':'))
            diffs.append(f"{new_path} : {old_val} -> <missing>")

        else:
            v1 = obj1[key]
            v2 = obj2[key]

            if isinstance(v1, dict) and isinstance(v2, dict):
                diffs.extend(deep_diff(v1, v2, new_path))
            elif v1 != v2:
                old_val = json.dumps(v1, separators=(',', ':'))
                new_val = json.dumps(v2, separators=(',', ':'))
                diffs.append(f"{new_path} : {old_val} -> {new_val}")

    return diffs


# Read input
obj1 = json.loads(sys.stdin.readline())
obj2 = json.loads(sys.stdin.readline())

differences = deep_diff(obj1, obj2)
differences.sort()

if differences:
    print("\n".join(differences))
else:
    print("No differences")