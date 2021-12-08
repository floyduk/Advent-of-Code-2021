import fileinput

count_unique_digits = 0
for line in fileinput.input():
    # Get the 4 digits from the input
    (line_part1, line_part2) = line.split(" | ")
    line_part2 = line_part2.strip()
    digits = line_part2.split()

    # Make a new list containing only digits with unique string length and count them
    unique_digits = [d for d in digits if len(d) in [2, 3, 4, 7]]
    count_unique_digits += len(unique_digits)

print("Solution: ", count_unique_digits)
