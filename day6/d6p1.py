import fileinput

# Input all starting data
fishes = list()
for line in fileinput.input():
    fishes = line.split(",")

# Convert fishes to integers
fishes = [int(fish) for fish in fishes]

print("Initial state: ", fishes)

for i in range(0, 256):
    # Decrement all counters
    fishes = [fish-1 for fish in fishes]

    # Count -1s
    append_fish_count = fishes.count(-1)

    # Replace all -1s with 6s
    fishes = [6 if fish == -1 else fish for fish in fishes]

    # Add new fishes
    for j in range(0, append_fish_count):
        fishes.append(8)

    print("After ", i+1, " days:")

print("Solution: ", len(fishes))