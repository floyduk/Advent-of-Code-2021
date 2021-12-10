import fileinput

# Load in the height map grid as a list of lists
grid = list()
local_minima = list()
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end
    grid.append([int(n) for n in list(line)])   # Convert string to list of integers

# Iterate the whole grid and at each point check up down left right for lower or equal heights
grid_height = len(grid)
grid_width = len(grid[0])
risk_level = 0
for y in range(0, grid_height):
    for x in range(0, grid_width):
        height_here = grid[y][x]

        # Check above
        if(y > 0):
            if(grid[y-1][x] <= height_here):
                continue

        # Check below
        if(y < grid_height-1):
            if(grid[y+1][x] <= height_here):
                continue

        # Check left
        if(x > 0):
            if(grid[y][x-1] <= height_here):
                continue

        # Check right
        if(x < grid_width-1):
            if(grid[y][x+1] <= height_here):
                continue

        # If we get here then this is a local minima
        local_minima.append((x, y))
        risk_level += height_here + 1

print("Solution:", risk_level)