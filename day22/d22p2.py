import fileinput
from typing import NamedTuple

class Range(NamedTuple):
    start: int
    end: int

class Cuboid(NamedTuple):
    on: bool
    x: Range
    y: Range
    z: Range


# Return the volume of Cuboid c
def cube_volume(c):
    return((c.x.end - c.x.start + 1) * (c.y.end - c.y.start + 1) * (c.z.end - c.z.start + 1))
    
# Return a Cuboid that is the intersection of Cuboids c1 and c2
def intersection_of(c1, c2, is_on):
    c = Cuboid(is_on, Range(max(c1.x.start, c2.x.start),min(c1.x.end, c2.x.end)),Range(max(c1.y.start, c2.y.start),min(c1.y.end, c2.y.end)),Range(max(c1.z.start, c2.z.start),min(c1.z.end, c2.z.end)))
    if c.x.end < c.x.start or c.y.end < c.y.start or c.z.end < c.z.start:
        return False
    else:
        return c

# Turn a line from the input file into a cuboid object and return it
def get_cuboid_from_line(line):
    cuboid = {}
    # Get the command
    (command, part2) = line.split(" ")

    # Get the ranges for each dimension and build a cuboid that represents the command
    ranges = part2.split(",")
    for range in ranges:
        (dimension, part2) = range.split("=")
        (range_start, range_end) = part2.split("..")

        # Make it so that range_start is always < range_end
        if int(range_start) <= int(range_end):
            cuboid[dimension] = Range(int(range_start), int(range_end))
        else:
            cuboid[dimension] = Range(int(range_end), int(range_start))

    return Cuboid(command == "on", Range(cuboid['x'].start, cuboid['x'].end), Range(cuboid['y'].start, cuboid['y'].end), Range(cuboid['z'].start, cuboid['z'].end))

cuboids = list()
# Read the commands list
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end

    c = get_cuboid_from_line(line)

    # Just so that I can see the work progressing
    print(f"{c}")

    # Keep new cuboids in a list so that we don't try and process them and get stuck in an infinite loop
    new_cuboids = list()

    # Step 1 find the intersections between the new cuboid and existing cuboids and make an inverse cuboid
    # for the intersecting area
    for oc in cuboids:
        i = intersection_of(c, oc, not oc.on)
        if i != False:
            new_cuboids.append(i)

    # Step 2 if this is an ON cuboid then add it
    if c.on:
        new_cuboids.append(c)

    # Add the new cuboids to the list of cuboids
    cuboids.extend(new_cuboids)

# Count ON cubes - OFF cubes and display result
size = 0
for c in cuboids:
    if c.on:
        size += cube_volume(c)
    else:
        size -= cube_volume(c)

print(f"Solution: {size}")