import fileinput

# One function that moves all the sea cucumbers in the direction given, "east" or "south"
def move(direction):
    global map, moves

    # Find all the direction facing sea cucumbers and make a list of the ones that feel they can move
    about_to_move = list()
    for y in range(0, map_height):
        for x in range(0, map_width):
            if direction == "east":
                if map[y][x] == ">":
                    if map[y][(x+1)%map_width] == ".":
                        about_to_move.append((x, y))
            else:
                if map[y][x] == "v":
                    if map[(y+1)%map_height][x] == ".":
                        about_to_move.append((x, y))

    # If there are any sea cucumbers about to move then set a flag to say so
    if len(about_to_move) > 0: moves = True
    
    # Move those sea cucumbers forward one step
    for (x, y) in about_to_move:
        map[y][x] = "."
        if direction == "east":
            map[y][(x+1)%map_width] = ">"
        else:
            map[(y+1)%map_height][x] = "v"

# Read the input data into the map array and take note of the dimensions
map = list()
for line in fileinput.input():
    line = line.rstrip()
    map.append(list(line))

map_width = len(map[0])
map_height = len(map)

# Iterate the moves until we find the final step
print(f"\Initial state:")
for r in map:
    print(''.join(r))
moves = True
count = 0
while moves:
    count += 1
    moves = False
    move("east")
    move("south")
    print(f"\nAfter {count} step{'s' if count > 1 else ''}:")
    for r in map:
        print(''.join(r))

print(f"Solution: {count}")