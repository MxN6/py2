import math


r = float(input())

x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1

a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - r*r

# Solve a t^2 + b t + c = 0
disc = b*b - 4*a*c

segment_length = math.sqrt(a)

if disc < 0:
    # No intersection
    # Entire segment inside or outside
    if c <= 0:
        print(f"{segment_length:.10f}")
    else:
        print("0.0000000000")
else:
    sqrt_disc = math.sqrt(disc)

    t1 = (-b - sqrt_disc) / (2*a)
    t2 = (-b + sqrt_disc) / (2*a)

    left = max(0.0, min(t1, t2))
    right = min(1.0, max(t1, t2))

    if right < 0 or left > 1:
        # No overlap with segment
        if c <= 0:
            print(f"{segment_length:.10f}")
        else:
            print("0.0000000000")
    else:
        overlap = max(0.0, right - left)
        print(f"{overlap * segment_length:.10f}")