import fileinput
from collections import Counter

# Take a string and turn it into a dictionary where keys are pairs of adjacent letters and value
# is the count of how many tiems that pair appear in the string.
def turn_into_letter_pairs(template):
    letter_pairs = {}
    for i in range(0, len(template) - 1):
        match = template[i:i+2]
        letter_pairs[match] = letter_pairs[match] + 1 if match in letter_pairs else 1
    return(letter_pairs)

# This function does most of the real work involved in d14p1. It runs along the string matching
# and inserting chars according to the rules. It builds the result into a new_template string
# which is passed back at the end. 
def grow_polymer(letter_pairs, rules, letter_count):
    new_letter_pairs = {}
    for match in letter_pairs.keys():
        # This is how many letters we're about to insert to our polymer
        count = letter_pairs[match]

        # Each time we insert a letter we're creating 2 new letter pairs
        if rules[match][0] in new_letter_pairs:
            new_letter_pairs[rules[match][0]] += count
        else:
            new_letter_pairs[rules[match][0]] = count

        if rules[match][1] in new_letter_pairs:
            new_letter_pairs[rules[match][1]] += count
        else:
            new_letter_pairs[rules[match][1]] = count

        # We just added count new letters to the polymer. Increase the letter count. 
        # The letter we added is the second letter in the first letter pair we added.
        # The Counter type returns 0 for items that aren't yet in the index, which means we
        # can just create new index items with one command like this. Very tidy.
        letter_count[rules[match][0][1]] += count

    return(new_letter_pairs)

# Rules is a dictionary with the match string as key and insertion string as value.
# Template is the polymer string that we will starting from. Once it's loaded we'll turn it 
# into a letter_pairs dictionary and we'll actually process that
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
        
        # For part 2 instead of storing the insert char we store the 2 resulting pairs from
        # inserting the insert char between the match chars. So rules is a dictionary where
        # the key is still the match string but the value is a tuple containing the 2 resulting
        # character pairs. See grow_polymer() to find out how this is used.
        rules[match] = (match[0] + insert, insert + match[1])
    else:
        # If nothing else matches then this must be the starting template
        template = line

# Turn our template into a dictionary of letter pairs with a count of how many times each pair 
# occurs in the final polymer string
letter_pairs = turn_into_letter_pairs(template)

# Our letter pairs data doesn't tell us the count of each letters, which we need for the solution
# so I make a separate letter_count object using the Counter type. When we run a rule we are
# Essentially just adding a single letter. NN becomes NC and CN but we only added a single C to
# the letter count. The count of Ns doesn't change.
letter_count = Counter(template)
print("Starting pairs: ", letter_pairs)
print("Starting letter count: ", letter_count)

# Grow the polymer n times
for step in range(0, 40):
    letter_pairs = grow_polymer(letter_pairs, rules, letter_count)
    print(f"After step {step+1}:\n{letter_pairs}\n{letter_count}")

# I use the Counter type from collections here because it does almost exactly what I need.
# I use it to count instances of each letter in our template and then the most_common() call
# returns a list of chars with their counts that I can inspect to get the numbers I need.
most_common = letter_count.most_common()[0]
least_common = letter_count.most_common()[-1]
print(f"{most_common}, {least_common}, difference = {most_common[1] - least_common[1]}")
