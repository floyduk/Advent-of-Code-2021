from typing import NamedTuple
import math

class TargetRange(NamedTuple):
    min: int
    max: int

# Sample.txt: target area: x=20..30, y=-10..-5
#target_x = TargetRange(20, 30)
#target_y = TargetRange(-10, -5)

# Input.txt: target area: x=81..129, y=-150..-108
target_x = TargetRange(81, 129)
target_y = TargetRange(-150, -108)

# Find all the dy values that hit the target in the range range_start..range_end
def iterate_dy_until_we_hit_range(range_start, range_end):
    successful_dy_values = list()

    for i in range(range_start-1, range_end+1):
        dy = i

        y = 0
        while y > target_y.max:
            y += dy
            dy -= 1

        if target_y.min <= y <= target_y.max:
            successful_dy_values.append(i)

    return successful_dy_values

# Find all the dx values that hit the target in the range range_start..range_end
def iterate_dx_until_we_hit_range(range_start, range_end):
    successful_dx_values = list()

    for i in range(range_start, range_end+1):
        dx = i
        x, last_x = 0, -1
        while x < target_x.min and x != last_x:
            last_x = x
            x += dx
            dx -= 1 if dx > 0 else 0
        
        if target_x.min <= x <= target_x.max:
            successful_dx_values.append(i)

    return successful_dx_values

# Map the tragectory using dx and dy and if any point on the trajectory is in the target area
# then return True
def trajectory_hits_target(dx, dy):
    x, y = 0, 0

    # Stop once y is less than the target_y.max
    while not y < target_y.min:
        x += dx
        y += dy
        dx -= 1 if dx > 0 else 0
        dy -= 1

        if target_x.min <= x <= target_x.max and target_y.min <= y <= target_y.max:
            return True

    return False

# The list of x values in a trajectory are completely unaffected by the dy value vice versa is true
# for y values. So we can analyse just the dx or dy values and find a list of successful values
successful_dx_values = iterate_dx_until_we_hit_range(0, target_x.max)
successful_valocities = list()
print("Successful dx values: ", successful_dx_values, "\n")

successful_dy_values = iterate_dy_until_we_hit_range(target_y.min, 200)
successful_valocities = list()
print("Successful dy values: ", successful_dy_values, "\n")

# We know all the possible successful values so now we just need to know which ones work together
for dx in successful_dx_values:
    for dy in successful_dy_values:
        if trajectory_hits_target(dx, dy):
            successful_valocities.append((dx, dy))

print(f"Solution: {len(successful_valocities)}")