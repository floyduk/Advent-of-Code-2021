import fileinput

flash_count = 0                                 # The total number of flashes
grid = list()                                   # The grid of dumbo octopus energy levels

#----- function defs

# Increment the energy level of an octopus but not if it has already flashed (energy 0)
def increment_grid_location(x, y):
    # Return if this location is out of bounds
    if(x < 0 or y < 0):
        return()
    if(x > grid_width-1 or y > grid_height-1):
        return()

    # Return if this octopus has already flashed
    if(grid[y][x] == 0):
        return()

    # Everything looks valid so increase octopus energy level
    grid[y][x] += 1

# Mark an octopus as having flashed (set energy to 0)
# Then increment energy of adjascent octopuses that aren't at energy 0 (meaning they have already flashed)
def flash_octopus(x, y):
    # Mark this octopus as having flashed
    grid[y][x] = 0

    # Increment energy levels of adjacent octopuses
    increment_grid_location(x-1, y-1)
    increment_grid_location(x, y-1)
    increment_grid_location(x+1, y-1)
    increment_grid_location(x-1, y)
    increment_grid_location(x+1, y)
    increment_grid_location(x-1, y+1)
    increment_grid_location(x, y+1)
    increment_grid_location(x+1, y+1)

#----- main

# Read the grid into a list of lists. We will access this as grid[y][x]
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end
    grid.append([int(x) for x in list(line)])    # convert 10 chars into 10 single digit integers

# Pre-calculate some numbers we'll use a lot
grid_width = len(grid[0])
grid_height = len(grid)
grid_size = grid_width * grid_height

# Loop for 100 steps
# Each step has 3 phases:
#   1. Increment energy of all octopuses
#   2. Check for flashes and then induced flashes
#   3. Set all octopuses that flashed to energy level 0
# I started out marking flashed octopuses as energy -1 but then realized 0 is even better because
# step 1 means no octopus can be at energy 0 in step 2 unless it has flashed this step. This means
# that flashed octopuses will end this step at 0 and I don't need to do step 3.
for age in range (1, 1000):
    # Increment energy level of all octopuses
    for y in range(0, grid_height):
        for x in range(0, grid_width):
            grid[y][x] += 1

    # Check for flashes and then induced flashes
    # We iterate the grid again and again until no more flashes occur
    # flashes_this_loop is used to determine when to stop iterating the grid looking for induced flashes
    flashes_this_loop = 1
    flashes_this_step = 0
    while(flashes_this_loop > 0):
        flashes_this_loop = 0
        for y in range(0, grid_height):
            for x in range(0, grid_width):
                if(grid[y][x] > 9):
                    flashes_this_step += 1
                    flashes_this_loop += 1
                    flash_count += 1
                    flash_octopus(x, y)

    # Flashes_this_step is the number of flashes on this step - not the same as flashes_this_loop
    if(flashes_this_step == grid_size):
        print(f"All flashed on step {age}")
        break