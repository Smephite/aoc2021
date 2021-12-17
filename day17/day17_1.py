import sys, os
sys.path.append(os.path.abspath("."))
import aoc
import math

[x_area, y_area] =  aoc.aoc()[0][13:].split(", ")
[x_start, x_end] = x_area[2:].split("..")
[y_start, y_end] = y_area[2:].split("..")


def sgn(num):
    return 0 if num == 0 else 1 if num > 0 else -1

x_area = range(int(x_start), int(x_end)+1)
y_area = range(int(y_start), int(y_end)+1)

starting_pos = (0, 0)
# y_dot[t+1] = y_dot[t] - 1
# y_dot[t] = y_dot[0] - t 
# y[t] = t*(y_dot[0]-(t-1)/2) + y[0]= t*y_dot[0] - t^2/2 + t/2 
#      = -t^2/2 + t(y_dot[0] + 1/2 )

# x_dot[t+1] = sgn(x_dot[t])*max(0, abs(x_dot[t])-1)
# x_dot[t] = sgn(x_dot[0])*max(0, abs(x_dot[0])-t)
# x_dot[t] =!= 0 => abs(x_dot[0]) = t
# thus x[t] = x[abs(x_dot[0])] for t > x_dot[0]
# else
# x[t] = sgn(x_dot[0])*t*(abs(x_dot[0]) - (t-1)/2) + x[0]


# calculates the position of a probe with initial condition initial_dot after t
def calc_pos(initial_dot, t):
    t_x = t if initial_dot[0] > t else initial_dot[0]

    return (sgn(initial_dot[0])*t_x*(abs(initial_dot[0])-(t_x-1)/2), -t**2/2+t*(initial_dot[1] + 1/2))


def calc_y_hit(y_dot_0, y_1):
    # y_1 = -t^2/2 + t(y_dot[0] + 1/2 )
    # 0 = -t^2 / 2 + t(y_dot[0] + 1/2) - y_1
    a = -1/2
    b = y_dot_0 + 1/2
    c = -y_1
    sqrt = math.sqrt(b**2-4*a*c)

    return max((-b+sqrt)/(2*a), (-b-sqrt)/(2*a))


y_dot_0 = 0
failed = 0
max_max = 0
while failed < 1e3:
    y_dot_0 += 1
    max_t = 0
    for y in y_area:
        t = calc_y_hit(y_dot_0, y)
        if t != int(t):
            continue
        max_t = max(max_t, t)
    if max_t == 0:
        failed+=1
        continue
    failed = 0
    max_t = int(max_t)
    max_y = 0
    for t in range(max_t):
        (_, y) = calc_pos((0, y_dot_0), t)
        max_y = max(max_y, y)
    max_max = max(max_max, max_y)
print("The highest point reachable is at y=", int(max_max))