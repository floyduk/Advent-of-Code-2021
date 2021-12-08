import fileinput

def subtract_segments(str1, str2):
    return(str1.translate({ord(i): None for i in str2}))

answer_total = 0
for line in fileinput.input():
    # Get the 4 digits from the input
    line = line.rstrip()                 # Clean up any spare characters on the end
    (line_part1, line_part2) = line.split(" | ")
    digits = line_part1.split()
    answer = line_part2.split()

    # Sort the digits by length
    digits = sorted(digits, key=len)

    # Sort the letters in the digits - not sure if this is necessary but it's neat
    digits = [sorted(d) for d in digits]
    digits = ["".join(d) for d in digits]

    # Put in the ones we know
    digit_lookup = ["", "", "", "", "", "", "", "", "", ""] # Stores what each digit means
    digit_lookup[0] = "1"
    digit_lookup[1] = "7"
    digit_lookup[2] = "4"
    digit_lookup[9] = "8"

    # This is all done by subtracting the segments of 2 numbers and looking at
    # The number of segments remaining

    # Find numbers 6 and 3
    number1 = digits[0]
    for seek_digit in [x for x in digits if len(x) in [5, 6]]:
        subtraction_len = len(subtract_segments(seek_digit, number1))
        if(subtraction_len == 5):       # 6 - 1 -> 6 (differentiate from 9 and 0)
            digit_lookup[digits.index(seek_digit)] = "6"
        elif(subtraction_len == 3):     # 3 - 1 -> 3 (differentiate from 2 and 5)
            digit_lookup[digits.index(seek_digit)] = "3"

    # Find numbers 9 and 0
    number3 = digits[digit_lookup.index("3")]
    for seek_digit in [x for x in digits if len(x) == 6 and digit_lookup[digits.index(x)] == ""]:
        subtraction_len = len(subtract_segments(seek_digit, number3))
        if(subtraction_len == 1):       # 9 - 3 -> 9 (differentiate from 0)
            digit_lookup[digits.index(seek_digit)] = "9"
        else:                           # 0 - 3 -> 0 (differentiate from 9)
            digit_lookup[digits.index(seek_digit)] = "0"

    # Find numbers 2 and 5
    number6 = digits[digit_lookup.index("6")]
    for seek_digit in [x for x in digits if digit_lookup[digits.index(x)] == ""]:
        subtraction_len = len(subtract_segments(number6, seek_digit))
        if(subtraction_len == 1):       # 6 - 5 -> 5 (differentiate from 2)
            digit_lookup[digits.index(seek_digit)] = "5"
        else:                           # 6 - 2 -> 2 (differentiate from 5)
            digit_lookup[digits.index(seek_digit)] = "2"

    print("digits:", digits, "\n       ", digit_lookup)

    # Now use what we've learned to parse the answer digits

    # Sort the letters in the answer digits
    answer = [sorted(d) for d in answer]
    answer = ["".join(d) for d in answer]
    print("sorted letters in answer digits:", answer)

    # Iterate the answer digits looking up what they mean in the digits and digit_lookup lists
    answer_str = ""
    for answer_digit in answer:
        answer_str = answer_str + digit_lookup[digits.index(answer_digit)]

    # Convert the string into an int and add it all up
    answer_int = int(answer_str)
    answer_total += answer_int
    print("Answer: ", answer_str, ":", answer_int, "\n")

print("Solution: ", answer_total)
