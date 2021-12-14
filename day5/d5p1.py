from typing import NamedTuple
import fileinput

# Let's make a special data type for storing our points that makes our code cleaner
# NamedTuples allow us to name the items in a tuple which is a but like a struct
class Vector(NamedTuple):
    x1: int
    y1: int
    x2: int
    y2: int

# A function for incrementing the value of a grid space. We use this a lot.
def increment_grid_space(grid, x, y):
    if(grid[y][x] == "."):
        grid[y][x] = "1"
    else:
        grid[y][x] = str(int(grid[y][x]) + 1)

# Load in all the lines from the input file
vent_lines = list()
for line in fileinput.input():
    line = line.strip()
    p1, p2 = line.split(" -> ")
    x1, y1 = p1.split(",")
    x2, y2 = p2.split(",")      # It's times like these that I miss Perl
    vent_lines.append(Vector(int(x1), int(y1), int(x2), int(y2)))

# Find the max dimensions of the grid
# Assume min x and y is 0 - this might always be true but it pays to state your assumptions
max_x, max_y = 0, 0
for line in vent_lines:
    max_x = max_x if line.x1 <= max_x else line.x1
    max_x = max_x if line.x2 <= max_x else line.x2
    max_y = max_y if line.y1 <= max_y else line.y1
    max_y = max_y if line.y2 <= max_y else line.y2
print("max_x", max_x, " max_y", max_y)

# Create a grid of the discovered dimensions
grid = []
for y in range(0, max_y+1):
    grid.append(['.'] * (max_x+1))

# Iterate the lines, marking them on the grid
for line in vent_lines:
    # Draw the line on the grid
    if(line.x1 == line.x2):     # Vertical line
        if(line.y1 > line.y2):
            for i in range(line.y2, line.y1+1):
                increment_grid_space(grid, line.x1, i)
        else:
            for i in range(line.y1, line.y2+1):
                increment_grid_space(grid, line.x1, i)

    elif(line.y1 == line.y2):   # Horizontal line
        if(line.x1 > line.x2):
            for i in range(line.x2, line.x1+1):
                increment_grid_space(grid, i, line.y1)
        else:
            for i in range(line.x1, line.x2+1):
                increment_grid_space(grid, i, line.y1)
    
    # We don't handle diagonals in part 1

# Display the grid - only useful for the sample data
#for row in grid:
#    for space in row:
#        print(space, end='')
#    print()

# Count grid spaces that aren't "." or "1"
count = 0
for row in grid:
    for space in row:
        if(space != "." and space != "1"):
            count += 1

print("Solution:", count)