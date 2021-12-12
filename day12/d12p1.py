import fileinput

# NOTE: I assume that because there are large caves and small caves and there will be comparatively 
# few large caves then maybe, perhaps, there won't be any possible loops. I'll start off coding this
# without loop detection and we'll see easily enough if my assumption is right because the code will
# never end.

# The paths list contains a list of 2 item tuples (source, destination). Though they can also be
# used as (destination, source), ie we can drive either way along each path.
paths = list()

# These are listsof routes found. Each route is a list of caves. The routes list is the working list
# and routes are moved to successful_routes when they reach the end
routes = list()
successful_routes = list()

# This uses 2 list comprehensions to select from the list of paths only those paths that start or 
# end with the cave given as a parameter. 
def get_list_of_destinations(cave):
    r = [d[1] for d in paths if d[0] == cave]
    r.extend([d[0] for d in paths if d[1] == cave])
    return(r)

# Read the grid into a list of lists. We will access this as grid[y][x]
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end
    (source, destination) = line.split("-")     # Split each line into source and destination
    paths.append((source, destination))         # Create a new path using the source and destination

# Start searching for routes from the 'start' cave. Create a new route for each available path
routes.append(['start'])

# Now iterate the routes looking for more destinations until each route either reaches the end or 
# dies (because it tries to go back to a small cave)
for r in routes:
    #print(f"\nHandling route: {r}")
    # Get a list of possible destinations from here
    destinations = get_list_of_destinations(r[-1])

    # Iterate the possible destinations and maybe make new routes for each one
    for d in destinations:
        # Valid path if destination is a big cave or a small cave we've not visited
        if(d.isupper() or d not in r):
            # Create a new path containing everything in this path r plus the valid destination
            route_to_add = r.copy()         # Note we FORCE Python to make a fresh copy of this list
            route_to_add.append(d)

            if(d == 'end'):
                # Add to successful_routes list instead of working routes list
                successful_routes.append(route_to_add)
            else:
                # Add this new route to the end of the routes list
                routes.append(route_to_add)

            #print(f"Added route {route_to_add}")

print(f"Successful routes {len(successful_routes)}")