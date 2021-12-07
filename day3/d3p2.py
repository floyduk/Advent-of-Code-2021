import fileinput

# Make a new list where only the ones that have 0s in this column are included then count the entries in the new list
def find_digit_in_position(lines, n, mostorleast):
        templineslist = [x for x in lines if x[n] == "0"] # Using list comprehension makes this easy
        count_zeroes = len(templineslist)
        count_ones = len(lines) - count_zeroes
        if(mostorleast == "most"):
                return(0 if count_zeroes > count_ones else 1) # If there are an equal number then choose 1
        else:
                return(1 if count_zeroes > count_ones else 0) # If there are an equal number then choose 0

# First of all let's read in all the lines in the data
lines = list()
for line in fileinput.input():
        lines.append(line.rstrip())
len_of_first_line = len(lines[0])

# Find the oxygen generator rating by looking for most common digits in each place and defaulting to 1 if they are equal
newlines = lines
for i in range(0, len_of_first_line):
        most_common = find_digit_in_position(newlines, i, "most")
        newlines = [x for x in newlines if x[i] == str(most_common)]
        if len(newlines) == 1:
                print("most common  ", most_common, " ", newlines)
                break
        print("most common  ", most_common, " ", newlines)
oxygen_generator_rating = int(newlines[0], 2)

# Find the CO2 scrubber rating by looking for least common digits in each place and defaulting to 0 if they are equal
newlines = lines
for i in range(0, len_of_first_line):
        least_common = find_digit_in_position(newlines, i, "least")
        newlines = [x for x in newlines if x[i] == str(least_common)]
        if len(newlines) == 1:
                print("least common  ", least_common, " ", newlines)
                break
        print("least common  ", least_common, " ", newlines)
co2_scrubber_rating = int(newlines[0], 2)

# Display the results
print(oxygen_generator_rating, " ", co2_scrubber_rating, " solution: ", (oxygen_generator_rating * co2_scrubber_rating))