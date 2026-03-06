n = int(input())

for _ in range(n):
    module_path, attr_name = input().split()
    try:
        # dynamically import module using exec
        exec(f"import {module_path} as mod")
        mod_obj = locals()['mod']
    except ModuleNotFoundError:
        print("MODULE_NOT_FOUND")
        continue

    if not hasattr(mod_obj, attr_name):
        print("ATTRIBUTE_NOT_FOUND")
    else:
        attr = getattr(mod_obj, attr_name)
        print("CALLABLE" if callable(attr) else "VALUE")