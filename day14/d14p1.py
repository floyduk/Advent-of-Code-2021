import fileinput
from collections import Counter

# This function does most of the real work involved in d14p1. It runs along the string matching
# and inserting chars according to the rules. It builds the result into a new_template string
# which is passed back at the end. 
def grow_polymer(template, rules):
    new_template = template[0]
    for i in range(0, len(template) - 1):
        match = template[i:i+2]
        new_template = new_template + rules[match] + template[i+1]
    return(new_template)

# Rules is a dictionary with the match string as key and insertion string as value.
# Template is the polymer string that we will be working on
rules = {}
template = ""

# Load in the starting template and then the insertion rules
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end

    if line == "":
        # Skip over blank lines
        continue
    elif " -> " in line:
        # Lines containing insertion rules have an arrow in them
        (match, insert) = line.split(" -> ")
        rules[match] = insert
    else:
        # If nothing else matches then this must be the starting template
        template = line

# Grow the polymer n times
for step in range(0, 10):
    print(f"{step}")
    template = grow_polymer(template, rules)

# I use the Counter type from collections here because it does almost exactly what I need.
# I use it to count instances of each letter in our template and then the most_common() call
# returns a list of chars with their counts that I can inspect to get the numbers I need.
counter = Counter(template)
most_common = counter.most_common()[0]
least_common = counter.most_common()[-1]
print(f"{most_common}, {least_common}, difference = {most_common[1] - least_common[1]}")
