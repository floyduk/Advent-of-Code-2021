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

# Part 2 added more logic that says in any valid route 1 small cave can be visited twice. So I
# replaced my single if statment from part 1 with this function which begins by doing much the 
# same thing then gets into the double visit stuff. Basically this function determines whether 
# this route is allowed to go to this destination. It looks at the data in the route to help make 
# that decision.
def is_valid_destination(route, destination):
    # Can never go back to the start    
    if(destination == 'start'):
        return(False)
    
    # End is always a valid destination
    if(destination == 'end'):
        return(True)
    
    # If destination is a big cave then it is always valid
    if(destination.isupper()):
        return(True)
    else:
        # If destination is a small cave and we've not been there yet then destination is valid
        if(destination not in route):
            return(True)

    # To arrive here the destination must be a small cave that we have already visited
    # so we must check for existing duplicate small caves. If there aren't any yet then
    # this destination is valid
    for r in route:
        # Return false if we find a small cave that appears more than once in the route
        if(not r.isupper() and route.count(r) > 1):
            return(False)

    # If we reach here then we did not find a duplicate and this is a valid destination
    return(True)


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
    # Get a list of possible destinations from here
    destinations = get_list_of_destinations(r[-1])

    # Iterate the possible destinations and maybe make new routes for each one
    for d in destinations:
        # Valid path if is_valid_destination says so. 
        # Part 2 added more logic here so I made it a function. Check function comments for explanation.
        if(is_valid_destination(r, d)):
            # Create a new path containing everything in this path r plus the valid destination
            route_to_add = r.copy()         # Note we FORCE Python to make a fresh copy of this list
            route_to_add.append(d)

            if(d == 'end'):
                # Add to successful_routes list instead of working routes list
                successful_routes.append(route_to_add)
            else:
                # Add this new route to the end of the routes list
                routes.append(route_to_add)

# All done.
print(f"Successful routes {len(successful_routes)}")