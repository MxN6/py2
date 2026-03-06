import math

r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1
a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - r*r

seg_len = math.hypot(dx, dy)

disc = b*b - 4*a*c

if disc <= 0:
    # segment completely outside circle
    print(f"{seg_len:.10f}")
else:
    # compute intersection t-values
    sqrt_disc = math.sqrt(disc)
    t1 = (-b - sqrt_disc)/(2*a)
    t2 = (-b + sqrt_disc)/(2*a)

    if t2 < 0 or t1 > 1:
        # intersection outside segment → segment fully outside
        print(f"{seg_len:.10f}")
    else:
        # segment crosses circle → tangent + arc needed
        # compute tangent lengths from A and B
        d1 = math.hypot(x1, y1)
        d2 = math.hypot(x2, y2)
        t1_len = math.sqrt(d1*d1 - r*r)
        t2_len = math.sqrt(d2*d2 - r*r)

        theta1 = math.atan2(y1, x1)
        theta2 = math.atan2(y2, x2)
        alpha1 = math.acos(r/d1)
        alpha2 = math.acos(r/d2)

        # external tangent path
        def normalize(a):
            while a < 0: a += 2*math.pi
            while a > 2*math.pi: a -= 2*math.pi
            return a

        arc1 = normalize((theta2 - alpha2) - (theta1 + alpha1))
        arc2 = normalize((theta2 + alpha2) - (theta1 - alpha1))
        angle_arc = min(arc1, 2*math.pi - arc1, arc2, 2*math.pi - arc2)

        length = t1_len + t2_len + r*angle_arc
        print(f"{length:.10f}")