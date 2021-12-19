import fileinput
from typing import NamedTuple

# Return x, y, z in various differnet rotation based on the orientation number
# Imagine your scanner as a cube. One side is marked with an X. There are 6 sides to the cube, so 6 
# directions that X could point in. And for each direction there are 4 rotations around the X axis.  
# 4 * 6 = 24 - which is the number we're looking for. But now to figure out what those 24 orientations 
# look like in code
def rotate(x, y, z, orientation):
    match orientation:
        case 0: return(x, y, z)
        case 1: return(x, -y, -z)
        case 2: return(-x, y, -z)
        case 3: return(-x, -y, z)
        case 4: return(x, z, -y)
        case 5: return(x, -z, y)
        case 6: return(-x, z, y)
        case 7: return(-x, -z, -y)
        case 8: return(y, z, x)
        case 9: return(y, -z, -x)
        case 10: return(-y, z, -x)
        case 11: return(-y, -z, x)
        case 12: return(y, x, -z)
        case 13: return(y, -x, z)
        case 14: return(-y, x, z)
        case 15: return(-y, -x, -z)
        case 16: return(z, x, y)
        case 17: return(z, -x, -y)
        case 18: return(-z, x, -y)
        case 19: return(-z, -x, y)
        case 20: return(z, y, -x)
        case 21: return(z, -y, x)
        case 22: return(-z, y, x)
        case 23: return(-z, -y, -x)
    print("SOMETHING WENT WRONG")
    exit()

# Build a dictionary of dictionaries. Keys to the outer are beacons. Keys to the inner are other 
# beacons. Values are diffs between them.
def build_differences(beacon_data):
    diffs = {} 
    for a in beacon_data:
        diffs[a] = {}
        for b in beacon_data:
            if a == b: continue
            diffs[a][b] = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    return diffs

# Compare two sets of diffs and return True if 12 or more match
def match_diffs(diffs1, diffs2):
    d1, d2 = list(diffs1.values()), list(diffs2.values())

    #print(f"Diffs1: {d1}\nDiffs2: {d2}\n")

    # First check if there is any intersection
    intersection = set(d1).intersection(d2)
    #print(f"Intersection: {intersection}")

    # NOTE: 11 diffs is 12 beacons because each diff has a source and desitnation but the source is 
    # the same for each diff
    if(len(intersection) >= 11):
        matches = [[],[]]
        # If there is an intersection then iterate the dictionaries and take note of the matches
        for a in diffs1.keys():
            for b in diffs2.keys():
                if diffs1[a] == diffs2[b]:
                    # Get the offset of scanner b from scanner a
                    # Yes it's the KEYS I want to subtract here because those are the coordinates of the beacon
                    offset = ((a[0] - b[0], a[1] - b[1], a[2] - b[2]))
                    matches[0].append(a)
                    matches[1].append(b)

        return((True, matches, offset))
    else: 
        return((False, [], ()))

# A scanner object that encapuslates all the data we know about a scanner and provides some basic 
# interfaces to work with that data
class Scanner:
    # Create the scanner based on a set of beacon data
    def __init__(self, beacon_data):
        self.beacon_data = beacon_data
        self.orientation = 0
        self.offset = (0,0,0)

    def set_offset(self, t):
        self.offset = t

    def set_orientation(self, o):
        self.orientation = o

    def get_offset(self):
        return self.offset

    def get_orientation(self):
        return self.orientation

    def add_beacon(self, b):
        if(b not in self.beacon_data):
            self.beacon_data.append(b)

    def get_number_of_beacons(self):
        return(len(self.beacon_data))

    # Return a set of rotated beacon data
    def get_beacon_data_at_orentation(self, orientation):
        return [rotate(b[0], b[1], b[2], orientation) for b in self.beacon_data]

    # Compare self.beacon_data to an other_beacon_data set
    def match_other_data_set(self, other_beacon_data):
        # Build the diffs here because they're going to be different for each orientation
        my_diffs = build_differences(self.beacon_data)
        other_beacon_diffs = build_differences(other_beacon_data)

        for k1 in my_diffs.keys():
            for k2 in other_beacon_diffs.keys():
                (result, matches, offset) = match_diffs(my_diffs[k1], other_beacon_diffs[k2])
                if(result):
                    matches[0].append(k1)
                    matches[1].append(k2)

                    return((result, matches, offset))

        return((False, [], ()))


# Load the source data in from a file
def load_input_data():
    global scanner_data

    for line in fileinput.input():
        line = line.rstrip()                        # Clean up any spare characters on the end

        if line == "": 
            scanner_data.append(Scanner(new_beacon_data))

        elif line.startswith("---"):
            new_beacon_data = list()
        
        else:
            new_beacon_data.append(tuple([int(n) for n in line.split(",")]))

    scanner_data.append(Scanner(new_beacon_data))

# Calculate and return the manhattan distance between 2 points
def manhattan_distance(a, b):
    return(abs(b[0] - a[0]) + abs(b[1] - a[1]) + abs(b[2] - a[2]))

# ---------------------------------------------------------------------------------------------
# ----------------------------------------- MAIN ----------------------------------------------
# ---------------------------------------------------------------------------------------------

# List of scanners each with a list of beacon locations
scanner_data = list()
load_input_data()

# A list of scanners that we've not matched yet. Start at 1 because we will always compare with
# scanner 0
scanners_to_match = list(range(1, len(scanner_data)))
while len(scanners_to_match) > 0:

    # Take the next unmatched scanner and try to match it with scanner 0
    for j in scanners_to_match:

        # Turn the data in every possible direction until we get a match
        for o in range(0, 24):
            # Get the other scanner beacon data in orientation o
            other_scanner_beacon_data = scanner_data[j].get_beacon_data_at_orentation(o)

            # Compare tha other scanner to scanner 0
            (result, matches, offset) = scanner_data[0].match_other_data_set(other_scanner_beacon_data)
            if result:
                print(f"MATCHED scanner {j} orientation {o} at offset {offset}")

                # If we got a match then drop other scanner off the list and record what we know in
                # the other scanner object
                scanners_to_match.remove(j)
                scanner_data[j].set_offset(offset)
                scanner_data[j].set_orientation(o)

                # Add to scanner 0 the beacons that DIDN'T get matched. They are new information.
                for b in other_scanner_beacon_data:
                    if b not in matches:
                        b = (b[0] + offset[0], b[1] + offset[1], b[2] + offset[2])
                        scanner_data[0].add_beacon(b)

# Calculate manhattan distanced between scanners
max_manhattan_distance = 0
for i in range(0, len(scanner_data)):
    for j in range(0, len(scanner_data)):
        if i == j: continue
        this_manhattan_distance = manhattan_distance(scanner_data[i].get_offset(), scanner_data[j].get_offset())
        max_manhattan_distance = this_manhattan_distance if this_manhattan_distance > max_manhattan_distance else max_manhattan_distance
        print(f"Manhattan distance between {i} and {j}: {this_manhattan_distance}")

print("Solution: ", max_manhattan_distance)