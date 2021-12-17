from typing import NamedTuple
import math
import pygame

# This is not part of the day 17 part 1 solution. See the pygame stuff at the end to understand
# why this is here.
pygame.init()
screen = pygame.display.set_mode([500,500])
running = True

# Create a tuple with named values to make the code more readable later
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
    global max_y

    x, y = 0, 0
    points = list()

    # Stop once y is less than the target_y.max
    while not y < target_y.min:
        x += dx
        y += dy
        dx -= 1 if dx > 0 else 0
        dy -= 1

        if y > max_y:
            max_y = y

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
max_y = 0
for dx in successful_dx_values:
    for dy in successful_dy_values:
        if trajectory_hits_target(dx, dy):
            successful_valocities.append((dx, dy))

print(f"Solution: {max_y}")

# ------------------------------

# All this stuff is to prove to myself that there cannot be any massive dy value that might cause the probe 
# to go way way up and then come down super fast at and hit the target zone. So to explain what you're seeing
# when you run this -  the black horizontal line is y=0 and the x axis plots dy values starting with 0 on the 
# left up to 500 on the right. The radial lines you see are the discrete points on the arc described by the 
# movement in the y plane of the probe. If it were possible for a high value to hit the target we wouldn't 
# see a solid line going at a 45 degree downward angle like we do at the bottom right. We would see some 
# scattered points or a much shallower line that trends towards the green zone. But the maths of this arc are 
# such that no discrete landing point can ever hit the green target zone. There are no lines that could trend 
# that way.

graph_done = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))

    if not graph_done:
        # Draw y = 0
        pygame.draw.line(screen, (255,0,0), (0, 250), (500, 250))

        # Draw the target zone
        pygame.draw.rect(screen, (0,255,0), (0, 250-target_y.max, 500, target_y.max - target_y.min))
        
        x = 0
        for i in range(0, 500):
            y, dy = 0, i
            points = []


            while not y < target_y.min:
                y += dy
                dy -= 1
                points.append(y)

            

            # Draw a dot on the graph for each point in the list
            print(f"Plotting x:{x} = {i}: {points[:10]} - {len(points)} points")
            for p in points:
                pygame.draw.circle(screen, (0,0,0), (x, 250-p), 1)
                if i == 7:
                    print(f"Plotting point {x}, {p}")

            x += 1
        pygame.display.flip()
        graph_done = True

pygame.quit()