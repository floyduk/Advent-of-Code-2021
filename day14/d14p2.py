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

# This function does most of the real work involved in d14p2. We work now with letter pairs so we
# take as input the dictionary of letter pairs where the key is the letter pair and the value is
# the count of times that pair appears in our polymer chain. Our rules have changed since part 1
# also. The rules dictionary's value now contain a tuple containing the two letter pairs created 
# by adding a letter in between the starting pair. So rule NN -> C means key 'NN' creates 'NC' and 
# 'CN'. So we iterate the pairs and for each we look up the rule that matches them. Into a new 
# dictionary we add the created letter pairs with the same count value as the starting pair had.
def grow_polymer(letter_pairs, rules):
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
print("Starting pairs: ", letter_pairs)

# Grow the polymer n times
for step in range(0, 40):
    letter_pairs = grow_polymer(letter_pairs, rules)
    print(f"After step {step+1}:\n{letter_pairs}")

# Thanks to @bitsofeight on the Club Twit discord for this idea. When I wrote this I felt that 
# there must be a way to get the letter count from the letter_pairs data and of course there is.
# You just need the first letter of each pair AND the last letter of the starting template - because
# the first and last letters never change and the last letter isn't the first letter of a pair.
letter_count = Counter()
for key in letter_pairs.keys():             # Add the first letter of each letter pair
    letter_count[key[0]] += letter_pairs[key]
letter_count[template[-1]] += 1             # Add the last letter of the starting template
most_common = letter_count.most_common()[0]
least_common = letter_count.most_common()[-1]
print(f"{most_common}, {least_common}, difference = {most_common[1] - least_common[1]}")
