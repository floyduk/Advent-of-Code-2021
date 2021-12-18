import fileinput
import math

# Show or hide debugging data
debug_reduction_steps = False
debug_additon_steps = False
debug_show_magnitudes = False

# First thoughts:
# I could try to come up with some neato data structure to represent snail numbers, maybe even a class
# with methods that perform the snail number operations
# Or I could just keep snail numbers as strings and parse the string whenever I need to perform an
# action on it.
# Turning this into some neato data structure would actually make finding numbers to the left and right
# pretty hard. So I'm going to stick with the strings for now until maybe part 2 bites me in the ass and 
# forces me to do something else.

# Later thoughts:
# It's clear now that I've written it that this should have all been recursive. After writing the 
# calculate_magnitude() function recursively at the end it wasn't SO hard to do. That business of finding
# the next numbers to the left and right would have been a pig, though. So maybe my approach was simpler
# after all. I may never know, but this works so.. whatever.

# Adding snail numbers is super easy. Just a string operation
def add_snail_numbers(left, right):
    return "[" + left + "," + right + "]"

# Turn a snail number pair into 2 integers
def get_integers_from_snail_number(snail_number):
    (a, b) = snail_number.replace("[", "").replace("]", "").split(",")
    return((int(a), int(b)))

# Look for 2 digit or more numbers
def find_2_digit_numbers(current_snail_number):
    match_length, match_index, match = 0, 0, ""

    # Iterate throught he snail number looking for digits. If we find 2 digits consecutively 
    # then match to the end of the number and immediately replace it with a pair
    for n in range(0, len(current_snail_number)):
        if(current_snail_number[n] in "0123456789"):
            match_length += 1
            match = match + current_snail_number[n]
            match_index = n if match_index == 0 else match_index
        else:
            if match_length > 1:
                # Match found
                break
            else:
                # This was just another 1 length digit or not a digit at all
                match_length, match_index, match = 0, 0, ""

    if match_length > 1:
        a = str(math.floor(int(match)/2))
        b = str(math.ceil(int(match)/2))
        new_snail_number = current_snail_number[:match_index] + "[" + a + "," + b + "]" + current_snail_number[(match_index + match_length):]

        if debug_reduction_steps:
            print(f"After split:    {new_snail_number}")

        return((True, new_snail_number))
    else:
        return((False, current_snail_number))

# Look for pairs nested inside 4 pairs and then if any are found with a depth >4 explode the first deepest one. I didn't know if we'd ever
# see nesting depths of >5 or more so I wrote this to explode the deepest first. That may not, in fact, be correct. It may not even be possible
# to get depths >5.
def find_deepest_nested_pair(current_snail_number):
    deepest_depth = 0
    deepest_depth_index = 0
    current_depth = 0
    matched_pair = ""
    matching = False

    # Iterate through the snail number counting brackets and remembering the deepest nested point
    for n in range(0, len(current_snail_number)):
        if current_snail_number[n] == "[":
            current_depth += 1
            if current_depth > deepest_depth:
                deepest_depth = current_depth
                deepest_depth_index = n
                matched_pair = ""
                matching = True

        if current_depth == deepest_depth and matching:
            matched_pair = matched_pair + current_snail_number[n]

        if current_snail_number[n] == "]":
            current_depth -= 1
            matching = False

    if(deepest_depth > 4):
        # Turn the matched pair into integers a and b
        (a, b) = get_integers_from_snail_number(matched_pair)

        # Find the first numbers to the left and right to which we will add a and b
        (left_match_index, left_match) = find_number_to_the_left(current_snail_number, deepest_depth_index)
        (right_match_index, right_match) = find_number_to_the_right(current_snail_number, deepest_depth_index + len(matched_pair))

        # Start building the new_snail_number string
        new_snail_number = current_snail_number

        # Add b to the right matched number
        if right_match_index != 0:
            new_snail_number = new_snail_number[:right_match_index] + str(b + int(right_match)) + new_snail_number[(right_match_index + len(right_match)):]
        
        # Replace the matched pair with a 0
        new_snail_number = new_snail_number[:deepest_depth_index] + "0" + new_snail_number[(deepest_depth_index + len(matched_pair)):]

        # Add a to the left matched number
        if left_match_index != 0:
            new_snail_number = new_snail_number[:(left_match_index + 1)] + str(a + int(left_match)) + new_snail_number[(left_match_index + len(left_match) + 1):]
        
        if debug_reduction_steps:
            print(f"After explode:  {new_snail_number}")

        return((True, new_snail_number))
    else:
        return((False, current_snail_number))

# Search left starting from index and return the first number we find along with the index of where it starts
def find_number_to_the_left(current_snail_number, index):
    n = index
    left_match = ""
    matching = False
    left_match_index = 0

    while True:
        n -= 1

        # Stop if we hit the start of the current_snail_number
        if n < 0: break                 

        # If we're finding digits then store them and start matching
        if current_snail_number[n] in "0123456789":
            left_match = current_snail_number[n] + left_match
            matching = True

        # If we're matching and we find a non-digit then we're done matching
        elif matching and current_snail_number[n] not in "0123456789":
            left_match_index = n
            break

    return((left_match_index, left_match))

# Search right starting from index and return the first number we find along with the index of where it starts
def find_number_to_the_right(current_snail_number, index):
    n = index
    right_match = ""
    matching = False
    right_match_index = 0

    while True:
        n += 1

        # Stop if we hit the end of the current_snail_number
        if n >= len(current_snail_number): break                 

        # If we're finding digits then store them and start matching
        if current_snail_number[n] in "0123456789":
            right_match = right_match + current_snail_number[n]
            if not matching: right_match_index = n
            matching = True

        # If we're matching and we find a non-digit then we're done matching
        elif matching and current_snail_number[n] not in "0123456789":
            break

    return((right_match_index, right_match))

# Recursively calculate the total magnitude of this snail number. Calls step through the current_snail_number
# keeping the index of where they're up to. Indexes are passed in and back out and when a pair is discovered 
# via a new "[" this function calls itself to handle the new pair. When a "]"" is found the magnitude of the
# pair is calculated and passed back to the caller.
def calculate_magnitude(current_snail_number, index):
    value_str = ""
    values_list = list()

    while index < len(current_snail_number):
        index += 1
    
        if current_snail_number[index] == "[":
            # Recursively read the pair we just found. 
            # This moves us up to the char past the ] and returns the integer value of that pair
            (value_str, index) = calculate_magnitude(current_snail_number, index)

        elif current_snail_number[index] in "0123456789":
            value_str = value_str + current_snail_number[index]

        elif current_snail_number[index] == ",":
            # Found the end of a number so convert it to an int and save it
            values_list.append(int(value_str))
            value_str = ""

        elif current_snail_number[index] == "]":
            # Found the end of a number so convert it to an int and save it and break
            values_list.append(int(value_str))
            break

        else:
            # Something went wrong!
            print("SOMETHING WENT WRONG")
            exit()
        
    # There should be exactly 2 values in the values_list
    if(len(values_list) != 2):
        print("SOMETHING ELSE WENT WRONG")
        exit()
    
    # Calculate and return the magnitude of this pair
    return((str((3 * values_list[0]) + (2 * values_list[1])), index))

# This is the MAIN code from part 1. Add two snail numbers a and b using snail maths
def add_snail_numbers_and_reduce(a, b):
    # Perform the addition    
    if debug_additon_steps:
        print(f"  {a}\n+ {b}")
    current_snail_number = add_snail_numbers(a, b)

    # Reduce the current_snail_number
    reduction_actions_found = True
    while reduction_actions_found:
        reduction_actions_found = False

        # 1. Check for explodes - Find pairs nested inside 4 pairs
        (reduction_actions_found, current_snail_number) = find_deepest_nested_pair(current_snail_number)

        if(not reduction_actions_found):
            # Check for splits - Find 2 digit numbers
            (reduction_actions_found, current_snail_number) = find_2_digit_numbers(current_snail_number)

    if debug_additon_steps:
        print(f"= {current_snail_number}\n")

    return(current_snail_number)




# ---------------------------------------------------------------------------------------------
# ----------------------------------------- MAIN ----------------------------------------------
# ---------------------------------------------------------------------------------------------

# Read in snail numbers one by one, adding them to a list
snail_numbers = list()
for line in fileinput.input():
    new_snail_number = line.rstrip()                        # Clean up any spare characters on the end
    snail_numbers.append(new_snail_number)

# Now try all combinations of these snail numbers adding them a+b and b+a, calculating the magnitude 
# for each and keeping track of the largest
max_magnitude = 0
for a in snail_numbers:
    for b in snail_numbers:
        # Skip this pair if a and b are the same snail number
        if a == b:
            continue

        # Try a+b
        result = add_snail_numbers_and_reduce(a, b)
        magnitude = int(calculate_magnitude(result, 0)[0])
        max_magnitude = magnitude if magnitude > max_magnitude else max_magnitude
        if debug_show_magnitudes:
            print(f"a+b magnitude: {magnitude}")

        # Try b+a
        result = add_snail_numbers_and_reduce(b, a)
        magnitude = int(calculate_magnitude(result, 0)[0])
        max_magnitude = magnitude if magnitude > max_magnitude else max_magnitude
        if debug_show_magnitudes:
            print(f"b+a magnitude: {magnitude}")

#Calculate and display the magnitude of this final snail number
print(f"Solution: {max_magnitude}")