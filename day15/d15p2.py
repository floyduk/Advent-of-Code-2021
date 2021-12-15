from typing import NamedTuple
import heapq
import fileinput

# Dijkstra's Algoritm
# Mark all nodes unvisited. Create a set of all the unvisited nodes called the unvisited set.
#
# Assign to every node a tentative distance value: set it to zero for our initial node and to 
# infinity for all other nodes. The tentative distance of a node v is the length of the shortest 
# path discovered so far between the node v and the starting node. Since initially no path is 
# known to any other vertex than the source itself (which is a path of length zero), all other 
# tentative distances are initially set to infinity. Set the initial node as current.[15]
#
# For the current node, consider all of its unvisited neighbors and calculate their tentative 
# distances through the current node. Compare the newly calculated tentative distance to the 
# current assigned value and assign the smaller one. For example, if the current node A is 
# marked with a distance of 6, and the edge connecting it with a neighbor B has length 2, then 
# the distance to B through A will be 6 + 2 = 8. If B was previously marked with a distance 
# greater than 8 then change it to 8. Otherwise, the current value will be kept.
#
# When we are done considering all of the unvisited neighbors of the current node, mark the 
# current node as visited and remove it from the unvisited set. A visited node will never be 
# checked again.
#
# If the destination node has been marked visited (when planning a route between two specific 
# nodes) or if the smallest tentative distance among the nodes in the unvisited set is infinity 
# (when planning a complete traversal; occurs when there is no connection between the initial 
# node and remaining unvisited nodes), then stop. The algorithm has finished.
#
# Otherwise, select the unvisited node that is marked with the smallest tentative distance, set 
# it as the new current node, and go back to step 3.

# Handy little named tuple that makes code nicer to read later on
class Point(NamedTuple):
    x: int
    y: int

# Woo look at me all fancy and using lambdas. It's just a function really.
adjacents = lambda x, y: [Point(x,y+1), Point(x+1, y), Point(x, y-1), Point(x-1, y)]

# Is the given point within the bounds of our data grid?
def is_valid_coordinate(p):
    return(0 <= p.x < grid_width and 0 <= p.y < grid_height)

# Init some variables
grid = list()
starting_grid = list()

# Load in the starting grid data
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end

    # Turn the input lines into lists of ints and add them as rows to grid
    starting_grid.append([int(x) for x in line])

# Get the dimensions of the starting grid
starting_grid_width = len(starting_grid[0])
starting_grid_height = len(starting_grid)

# Copy the starting grid into the full grid
for row in starting_grid:
    grid.append(row.copy())

# Copy the starting grid 4 more times onto the end of the grid rows
for i in range(0, 4):
    for j in range(0, starting_grid_height):
        newlist = [(((a+i)%9)+1) for a in starting_grid[j]]
        grid[j].extend(newlist)

# Create 4 more sets of rows in the final grid
for i in range(0, 4):
    for j in range(0, starting_grid_height):
        newlist = [(((a+i)%9)+1) for a in grid[j]]
        grid.append(newlist)

# Get the dimensions of the final grid
grid_width = len(grid[0])
grid_height = len(grid)

# ---------- Dijkstra starts here ----------

# Add the source location to the list of points that need to be searched
search_points = []
heapq.heappush(search_points, (0, Point(0, 0)))

# Visit every node always choosing the lowest dist node and look at its adjacent nodes
# For each one set that adjacent node's cost to this node's cost plus the cost of the 
# adjacent node. Read the large comment at the top describing Dijkstra's algorithm for 
# more detailed explanation. The best description I found of how this works is on page:
# https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
# I didn't use their code but their description was the clearest I could find. 
# Following a little reading around I've modified this algorithm to use heapq, which is 
# a much better datatype for this use because search_points[0] will always be the lowest 
# cost queue item. Seems tailor made for the Dijkstra algorithm. 
# Also made a small change that I saw somewhere that adds the nodes to the queue as it 
# finds them rather than added them all at the start.
visited_nodes = set()
while search_points:
    cost, here = heapq.heappop(search_points)

    # If we've reached the destination then stop and show the answer
    if here == Point(grid_width -1, grid_height - 1):
        print("Solution: ", cost)
        exit()

    # Move on if this node has already been visited
    if here in visited_nodes: 
        continue

    # Add this point to the list of visited nodes
    visited_nodes.add(here)

    # Adjacent nodes
    for p in adjacents(here.x, here.y):
        # Move on if this adjacent node isn't valid
        if is_valid_coordinate(p):
            heapq.heappush(search_points, (cost + grid[p.y][p.x], p))