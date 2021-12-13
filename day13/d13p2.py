import fileinput

# Discover the grid size, create the grid, plot the points, and then display the grid
# Note: This is no longer just for testing or interest. For part 2 we need to see the 
# grid in order to get the answer.
def plot_and_display_the_grid():
    grid = list()
    grid_height = 0
    grid_width = 0
    
    # Discover the max x and y from the data
    for p in points:
        (x, y) = p
        grid_width = max(x, grid_width)         
        grid_height = max(y, grid_height)

    # Create an empty grid
    for y in range(0, grid_height+1):
        grid.append(['.'] * (grid_width+1))

    # Plot all the points on the grid
    for p in points:
        grid[p[1]][p[0]] = '#'

    # Display the grid
    print("\n")
    for g in grid:
        print(''.join(g))

# Fold along the x_or_y axis on line
# Note we never do this on the grid. We just take the list of points and translate them
# then place the new point into a new points list which we return. It's a simple arithmetical
# operation. We'll plot the final points onto a grid at the very end.
def fold_along(points, x_or_y, line):
    # Make a new points list
    new_points = list()
    for p in points:
        if x_or_y == "x":
            # Y stays the same. X translates to a new position
            x = p[0] if p[0] < line else (line - (p[0] - line))
            y = p[1]
        else:
            # X stays the same. Y translates to a new position
            x = p[0]
            y = p[1] if p[1] < line else (line - (p[1] - line))

        # Don't add it if this point already exists
        if((x, y) not in new_points):
            new_points.append((x, y))

    return(new_points)

# My approach:
# 1. Load in the points
# 2. Load in the rules
# 3. Process the rules - performing the folds
# 4. Plot the points onto a grid and display it

# The list of points and rules that we'll use throughout
points = list()
rules = list()

# Load in the points and the rules
loading_points = True                           # We are either loading the points or the rules
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end
    if line == "":
        # A blank line signals the switch from points to rules
        loading_points = False
    elif loading_points:
        # Parse the point x and y and append it to the points list
        (x, y) = [int(x) for x in line.split(",")]
        points.append((x, y))

    else:
        # Load rules
        (part1, part2) = line.split("=")        # I want the char before the = and everything after it
        part1 = part1[-1]                       # Grab the single char before the =
        rules.append((part1, int(part2)))

# Iterate the rules folding and folding
for r in rules:
    points = fold_along(points, r[0], r[1])

# Display the result
plot_and_display_the_grid()