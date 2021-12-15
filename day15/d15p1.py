from typing import NamedTuple
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

# A point type just to make the code cleaner
class Point(NamedTuple):
    x: int
    y: int

# Return true if this coordinate is within the grid
def is_valid_coordinate(p):
    return(p.x >= 0 and p.x < grid_width and p.y >= 0 and p.y < grid_height)

# Find the unvisited node with the lowest dist[][] value
def node_with_shortest_dist():
    shortest_dist = 99999

    for n in unvisited_nodes:
        if dist[n.y][n.x] < shortest_dist:
            shortest_dist = dist[n.y][n.x]
            shortest_dist_node = n

    return(shortest_dist_node)

# I'll input the grid or risk values into grid
grid = list()

# Load in the starting template and then the insertion rules
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end

    # Turn the input lines into lists of ints and add them as rows to grid
    grid.append([int(x) for x in line])

grid_width = len(grid[0])
grid_height = len(grid)

# Array of distances from source
dist = list()
for i in range(0, grid_height):
    dist.append([99999] * grid_width)

# Set the distance from the source to the source as 0
dist[0][0] = 0

# List of unvisited nodes
unvisited_nodes = list()
for y in range(0, grid_height):
    for x in range(0, grid_width):
        unvisited_nodes.append(Point(x, y))

# Visit every node always choosing the lowest dist node and look at its adjacent nodes
# For each one set that adjacent node's cost to this node's cost plus the cost of the 
# adjacent node. Read the large comment at the top describing Dijkstra's algorithm for 
# more detailed explanation. The best description I found of how this works is on page:
# https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
# I didn't use their code but their description was the clearest I could find. 
print("Unvisited nodes: ", len(unvisited_nodes))
while(len(unvisited_nodes) > 0):
    here = node_with_shortest_dist()

    # Adjacent nodes
    pd = Point(here.x, here.y+1)
    pr = Point(here.x+1, here.y)
    pu = Point(here.x, here.y-1)
    pl = Point(here.x-1, here.y)
    for p in [pd, pr, pu, pl]:
        # Move on if this adjacent node isn't valid
        if not is_valid_coordinate(p):
            continue

        # Move on if this adjacent node has already been visited
        if not p in unvisited_nodes:
            continue

        if dist[here.y][here.x] + grid[p.y][p.x] < dist[p.y][p.x]:
            dist[p.y][p.x] = dist[here.y][here.x] + grid[p.y][p.x]
    
    unvisited_nodes.remove(here)

    print("Unvisited nodes: ", len(unvisited_nodes))

# Print the distance (risk) in the destination cell. This is the shortest (least risky) path cost
print(dist[grid_height-1][grid_width-1])