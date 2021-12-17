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


trajectories = []
for y_dot_0 in range(y_area.start, abs(y_area.start)):
    for x_dot_0 in range(0, abs(x_area.stop)):
        for t in range(int(calc_y_hit(y_dot_0, y_area.stop)), int(calc_y_hit(y_dot_0, y_area.start)+1)):
            pos = calc_pos((x_dot_0, y_dot_0), t)
            if pos[0] in x_area and pos[1] in y_area:
                trajectories.append((x_dot_0, y_dot_0))
                break
            if pos[0] > x_area.stop or pos[1] < y_area.start:
                break



set = ((list(set(trajectories))))

print("There are", len(set), "different combinations.")

