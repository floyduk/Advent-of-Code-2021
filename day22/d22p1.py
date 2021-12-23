import fileinput
from typing import NamedTuple

class Range(NamedTuple):
    start: int
    end: int

class Cuboid(NamedTuple):
    x: Range
    y: Range
    z: Range

class Point(NamedTuple):
    x: int
    y: int
    z: int


# Turn a cuboid into a list of points - one at each corner
all_points = lambda c : [Point(c.x.start, c.y.start, c.z.start), Point(c.x.end, c.y.start, c.z.start), Point(c.x.start, c.y.end, c.z.start), Point(c.x.start, c.y.start, c.z.end), Point(c.x.end, c.y.end, c.z.start), Point(c.x.end, c.y.start, c.z.end), Point(c.x.start, c.y.end, c.z.end), Point(c.x.end, c.y.end, c.z.end)]

# Return the volume of Cuboid c
def cube_volume(c):
    return((c.x.end - c.x.start + 1) * (c.y.end - c.y.start + 1) * (c.z.end - c.z.start + 1))
    
# Return true if Cuboids c1 and c2 intersect
def cuboids_intersect(c1, c2):
    c1_points_inside_c2, c2_points_inside_c1 = 0, 0

    for p in all_points(c1):
        if c2.x.start <= p.x <= c2.x.end and c2.y.start <= p.y <= c2.y.end and c2.z.start <= p.z <= c2.z.end:
            c1_points_inside_c2 += 1
    
    for p in all_points(c2):
        if c1.x.start <= p.x <= c1.x.end and c1.y.start <= p.y <= c1.y.end and c1.z.start <= p.z <= c1.z.end:
            c2_points_inside_c1 += 1

    return (c1_points_inside_c2 > 0 or c2_points_inside_c1 > 0)

# Return a Cuboid that is the intersection of Cuboids c1 and c2
def intersection_of(c1, c2):
    return Cuboid(Range(max(c1.x.start, c2.x.start),min(c1.x.end, c2.x.end)),Range(max(c1.y.start, c2.y.start),min(c1.y.end, c2.y.end)),Range(max(c1.z.start, c2.z.start),min(c1.z.end, c2.z.end)))

# Subtract c1 from c2 and return the pieces that makes
# Thinking of this as a rubik's cube
# Cube 1 is top face back left and reading across and then down are cubes 2, 3, then 4, 5, 6, then 7, 8, 9
# Next layer down is 10, 11, 12 then 13, 14, 15, then 16, 17, 18
# And then bottom layer is 19-27 in the same arrangement
# top face is x, y. z dimension is down the cube. Origin is top left of cube 1.
def subtract_cuboid(c1, c2):
    i = intersection_of(c1, c2)

    # calculate the resulting cubes
    new_cubes = list()

    if c2.z.start < i.z.start:
        # Cubes 1, 2, 3, 4, 5, 6, 7, 8, 9
        if c2.y.start < i.y.start:    
            # Cubes 1, 2, 3
            if c2.x.start < i.x.start:
                new_cubes.append(Cuboid(Range(c2.x.start, i.x.start-1), Range(c2.y.start, i.y.start-1), Range(c2.z.start, i.z.start-1)))
            new_cubes.append(Cuboid(Range(i.x.start, i.x.end), Range(c2.y.start, i.y.start-1), Range(c2.z.start, i.z.start-1)))
            if c2.x.end > i.x.end:
                new_cubes.append(Cuboid(Range(i.x.end+1, c2.x.end), Range(c2.y.start, i.y.start-1), Range(c2.z.start, i.z.start-1)))

        # Cubes 4, 5, 6
        if c2.x.start < i.x.start:
            new_cubes.append(Cuboid(Range(c2.x.start, i.x.start-1), Range(i.y.start, i.y.end), Range(c2.z.start, i.z.start-1)))
        new_cubes.append(Cuboid(Range(i.x.start, i.x.end), Range(i.y.start, i.y.end), Range(c2.z.start, i.z.start-1)))
        if c2.x.end > i.x.end:
            new_cubes.append(Cuboid(Range(i.x.end+1, c2.x.end), Range(i.y.start, i.y.end), Range(c2.z.start, i.z.start-1)))

        if c2.y.end > i.y.end:
            # Cubes 7, 8, 9
            if c2.x.start < i.x.start:
                new_cubes.append(Cuboid(Range(c2.x.start, i.x.start-1), Range(i.y.end+1, c2.y.end), Range(c2.z.start, i.z.start-1)))
            new_cubes.append(Cuboid(Range(i.x.start, i.x.end), Range(i.y.end+1, c2.y.end), Range(c2.z.start, i.z.start-1)))
            if c2.x.end > i.x.end:
                new_cubes.append(Cuboid(Range(i.x.end+1, c2.x.end), Range(i.y.end+1, c2.y.end), Range(c2.z.start, i.z.start-1)))

    # Cubes 10, 11, 12, 13, 14, 15, 16, 17, 18
    if c2.y.start < i.y.start:    
        # Cubes 10, 11, 12
        if c2.x.start < i.x.start:
            new_cubes.append(Cuboid(Range(c2.x.start, i.x.start-1), Range(c2.y.start, i.y.start-1), Range(i.z.start, i.z.end)))
        new_cubes.append(Cuboid(Range(i.x.start, i.x.end), Range(c2.y.start, i.y.start-1), Range(i.z.start, i.z.end)))
        if c2.x.end > i.x.end:
            new_cubes.append(Cuboid(Range(i.x.end+1, c2.x.end), Range(c2.y.start, i.y.start-1), Range(i.z.start, i.z.end)))

    # Cubes 13, 14, 15
    if c2.x.start < i.x.start:
        new_cubes.append(Cuboid(Range(c2.x.start, i.x.start-1), Range(i.y.start, i.y.end), Range(i.z.start, i.z.end)))
    # This middle cube is the one we're removing! So let's not create it and add it to the new cubes list, eh?
    #new_cubes.append(Cuboid(Range(i.x.start, i.x.end), Range(i.y.start, i.y.end), Range(i.z.start, i.z.end)))
    if c2.x.end > i.x.end:
        new_cubes.append(Cuboid(Range(i.x.end+1, c2.x.end), Range(i.y.start, i.y.end), Range(i.z.start, i.z.end)))

    if c2.y.end > i.y.end:
        # Cubes 16, 17, 18
        if c2.x.start < i.x.start:
            new_cubes.append(Cuboid(Range(c2.x.start, i.x.start-1), Range(i.y.end+1, c2.y.end), Range(i.z.start, i.z.end)))
        new_cubes.append(Cuboid(Range(i.x.start, i.x.end), Range(i.y.end+1, c2.y.end), Range(i.z.start, i.z.end)))
        if c2.x.end > i.x.end:
            new_cubes.append(Cuboid(Range(i.x.end+1, c2.x.end), Range(i.y.end+1, c2.y.end), Range(i.z.start, i.z.end)))

    if c2.z.end > i.z.end:
        # Cubes 19, 20, 21, 22, 23, 24, 25, 26, 27
        if c2.y.start < i.y.start:    
            # Cubes 19, 20 ,21
            if c2.x.start < i.x.start:
                new_cubes.append(Cuboid(Range(c2.x.start, i.x.start-1), Range(c2.y.start, i.y.start-1), Range(i.z.end+1, c2.z.end)))
            new_cubes.append(Cuboid(Range(i.x.start, i.x.end), Range(c2.y.start, i.y.start-1), Range(i.z.end+1, c2.z.end)))
            if c2.x.end > i.x.end:
                new_cubes.append(Cuboid(Range(i.x.end+1, c2.x.end), Range(c2.y.start, i.y.start-1), Range(i.z.end+1, c2.z.end)))

        # Cubes 22, 23, 24
        if c2.x.start < i.x.start:
            new_cubes.append(Cuboid(Range(c2.x.start, i.x.start-1), Range(i.y.start, i.y.end), Range(i.z.end+1, c2.z.end)))
        new_cubes.append(Cuboid(Range(i.x.start, i.x.end), Range(i.y.start, i.y.end), Range(i.z.end+1, c2.z.end)))
        if c2.x.end > i.x.end:
            new_cubes.append(Cuboid(Range(i.x.end+1, c2.x.end), Range(i.y.start, i.y.end), Range(i.z.end+1, c2.z.end)))

        if c2.y.end > i.y.end:
            # Cubes 25, 26, 27
            if c2.x.start < i.x.start:
                new_cubes.append(Cuboid(Range(c2.x.start, i.x.start-1), Range(i.y.end+1, c2.y.end), Range(i.z.end+1, c2.z.end)))
            new_cubes.append(Cuboid(Range(i.x.start, i.x.end), Range(i.y.end+1, c2.y.end), Range(i.z.end+1, c2.z.end)))
            if c2.x.end > i.x.end:
                new_cubes.append(Cuboid(Range(i.x.end+1, c2.x.end), Range(i.y.end+1, c2.y.end), Range(i.z.end+1, c2.z.end)))

    # Delete any cubes that end up being 0 volume. There SHOULDN'T be any, though, so let's put a print in when there is.
#    count_matches = 0
#    for nc in new_cubes:
#        for oc in new_cubes:
#            if nc.x.start == oc.x.start and nc.x.end == oc.x.end and nc.y.start == oc.y.start and nc.y.end == oc.y.end and nc.z.start == oc.z.start and nc.z.end == oc.z.end:
#                count_matches += 1
#        if count_matches > 2:
#            print("SOMETHING BAD HAPPENED when subtracting {c1} from {c2}\n")
#            for c in new_cubes:
#                print(f"{c}")
#            exit()

    return(new_cubes)

# The reactor is a range of cubes. Regions of the reactor cubes are on or off and the
# ON cubes are stored in the cuboids list which is a list of type cuboid. Each cuboid is
# a dictionary with keys x, y, z and values of type Range. If I code this correctly cuboid
# list items will never overlap.
#cuboid = {‘x’: Range(x1, x2), ‘y’: Range(x1, x2), ‘z’:Range(x1, x2)}
cuboids = list()

# Read the commands list
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end
    (command, part2) = line.split(" ")

    # Get the ranges for each dimension and build a cuboid that represents the command
    cuboid = {}
    ranges = part2.split(",")
    for range in ranges:
        (dimension, part2) = range.split("=")
        (range_start, range_end) = part2.split("..")

        # Make it so that range_start is always < range_end
        if int(range_start) <= int(range_end):
            cuboid[dimension] = Range(int(range_start), int(range_end))
        else:
            cuboid[dimension] = Range(int(range_end), int(range_start))

    c = Cuboid(Range(cuboid['x'].start, cuboid['x'].end), Range(cuboid['y'].start, cuboid['y'].end), Range(cuboid['z'].start, cuboid['z'].end))

    # Check if this range intersects with -50..50 in any dimension
#    if not cuboids_intersect(c, Cuboid(Range(-50, 50), Range(-50, 50), Range(-50, 50))):
#        print(f"For part 1 solution discarding {c}")
#        continue

    # Perform the given command on the reactor cubes
    if command == "on":
        # COMMAND ON
        print(f"\nCOMMAND ON {c}")
        # Make a list of new cuboids to add starting with just the new ON cuboid. Then iterate through
        # the existing cuboids subtracting each one from the new ON cuboid and resulting in several 
        # smaller new ON cuboids until we've accounted for all the existing cuboids. Then add that 
        # list of new ON cuboids to the list of cuboids.
        cuboids_to_add = [c]
        go_again = True
        while(go_again):
            for existing_cuboid in cuboids:
                new_cuboids_to_add = list()
                for c in cuboids_to_add:
                    if cuboids_intersect(c, existing_cuboid):
                        print(f"ON Subtracting {existing_cuboid} from {c}")
                        new_cuboids_to_add.extend(subtract_cuboid(existing_cuboid, c))
                    else:
                        new_cuboids_to_add.append(c)
                cuboids_to_add = new_cuboids_to_add

            go_again = False
            for c in cuboids_to_add:
                for d in cuboids:
                    if c != d:
                        if cuboids_intersect(c, d):
                            go_again = True
                            print(f"ON - SOMETHING BAD HAPPENED - intersecting cuboids\n{c}\n{d}")

        cuboids.extend(cuboids_to_add)

    else:
        # COMMAND OFF
        print(f"\nCOMMAND OFF {c}")
        # Iterate the list of existing cuboids and if they intersect with the new OFF cuboid then
        # subtract the OFF cuboid from the existing cuboid and add it to the new_cuboids list. If
        # they don't intersect then add the existing cuboids to the new_cuboids list
        new_cuboids = list()
        for existing_cuboid in cuboids:
            if cuboids_intersect(c, existing_cuboid):
                print(f"OFF Subtracting {c} from {existing_cuboid}")
                new_cuboids.extend(subtract_cuboid(c, existing_cuboid))
            else:
                new_cuboids.append(existing_cuboid)

        cuboids = new_cuboids

    size = 0
    for c in cuboids:
        size += cube_volume(c)
    print(f"{size} cubes on")

#    for c in cuboids:
#        for d in cuboids:
#            if c != d:
#                if cuboids_intersect(c, d):
#                    print(f"SOMETHING BAD HAPPENED - intersecting cuboids\n{c}\n{d}")
#                    exit()


# Count ON cubes and display result
# This means adding up the sizes of all the cuboid in the cuboids list
size = 0
for c in cuboids:
    size += cube_volume(c)

print(f"Solution: {size}")


# NOTE: This code is an absolute mess. I'm leaving it that way because I went down so many dead ends
# writing it and eventually gave up on this approach entirely. This code will give the right answer for
# part 1 but it fails for part 2 and I just can't figure out why. The data is too big and complex to step
# through and find out where it's going wrong. Where you see SOMETHING BAD HAPPENED in the code was me
# trying to identify the moment it failed in order the debug it. There's a logic bug in here somewhere. I 
# don't believe this is an off by one error - not unless there's a typo in subtract_cuboid() somewhere. But
# I've looked carefully and I can't find it if it's there. 
# 
# So consider this code historical in so much as it's an example of something that was basically a successful
# idea but that was too complex to debug when something started going wrong.