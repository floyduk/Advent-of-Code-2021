import fileinput, math

# This function is passed the x, y of a local minima and searches outwards from there until it
# finds a basin edge. The edge is where the height becomes 9 (max) or where the height starts to 
# go downwards - that would be a new, different basin.
# The function uses several lists commented below. The main control loop iterates points_to_check
# which it pops the first item off and checks it before adding surrounding points to the list of
# points_to_check. Points are not checked if they have already been checked and placed on either
# the basin or basin_edge lists.
def find_basin(grid, x, y, width, height):
    basin_edge = list()         # A list of points that are NOT part of this basin
    basin = list()              # A list of points that ARE part of this basin
    points_to_check = list()    # A list of points that we still need to check before we're done

    # Add the starting point to our list of points_to_check
    height_here = grid[y][x]
    points_to_check.append((x, y, height_here))

    # Iterate the list of points to check until the list is empty
    while(len(points_to_check) > 0):
        # Get the first point to check from the list and then delete it from the list
        (point_x, point_y, previous_height) = points_to_check[0]
        del points_to_check[0]
        point_height = grid[point_y][point_x]

        # Move on immediately if this point is already in the basin or basin edge list
        if((point_x, point_y) in basin or (point_x, point_y) in basin_edge):
            continue

        # If point_height is 9 or point_height < height_here then add to basin_edge list
        if(point_height == 9 or point_height < previous_height):
            basin_edge.append((point_x, point_y))
            continue
        
        # Otherwise add point to this basin
        basin.append((point_x, point_y))

        # Now add points to check for adjascent points
        if(point_x > 0):
            points_to_check.append((point_x-1,point_y,height_here))
        if(point_x < width-1):
            points_to_check.append((point_x+1,point_y,height_here))
        if(point_y > 0):
            points_to_check.append((point_x,point_y-1,height_here))
        if(point_y < height-1):
            points_to_check.append((point_x,point_y+1,height_here))

    # If len(points_to_check) is 0 then we've finished mapping this basin
    basin_size = len(basin)

    # For day9 I actually only need the basin_size but I worked hard to get 
    # that basin data so I'm darn well going to pass it back!
    return((basin_size, basin))

# Load in the height map grid as a list of lists
grid = list()
local_minima = list()
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end
    grid.append([int(n) for n in list(line)])   # Convert string to list of integers
    grid_height = len(grid)
    grid_width = len(grid[0])

# Iterate the grid looking for local minima (low points)
for y in range(0, len(grid)):
    for x in range(0, len(grid[0])):
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

# Iterate all the local minima we found and find the basins around them
basin_sizes = list()
for point in local_minima:
    (basin_size, basin) = find_basin(grid, point[0], point[1], grid_width, grid_height)
    basin_sizes.append(basin_size)

# Find the 3 largest basins
print("Biggest 3 basin sizes: ", sorted(basin_sizes)[-3:])
biggest_3 = sorted(basin_sizes)[-3:]
solution = math.prod(biggest_3)

print("Solution: ", solution)