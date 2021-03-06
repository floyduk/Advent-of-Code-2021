import fileinput

chunk_openers = ["(", "[", "{", "<"]
chunk_closers = [")", "]", "}", ">"]
chunk_values = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

# Read the file line by line
corrupted_line_chars = list()                   # Keep a list of corrupted chars because they're used for scoring
for line in fileinput.input():
    line = line.rstrip()                        # Clean up any spare characters on the end
    line = list(line)                           # Convert to array of chars for easier iteration

    # Run through the line char by char keeping track of opens and closes
    opens = list()                              # A list containing, in order, the chunk openers we've seen so far on this line
    line_state = "valid"                        # Just used so that I can decide what to do with this line after parsing it
    for c in line:
        if(c in chunk_openers):
            # Open a chunk
            opens.append(c)
        elif(c in chunk_closers):
            # Trying to close a chunk - is this the correct chunk closer?
            expected_closer = chunk_closers[chunk_openers.index(opens[-1])]
            if(c != expected_closer):
                # Corrupted line
                print("Corrupted line: expected ", expected_closer, " but found ", c)
                line_state = "corrupted"
                corrupted_line_chars.append(c)
                break
            else:
                # Closing a chunk
                del(opens[-1])

    # If we reach here without the line being corrupted but we have remaining opens then it is incomplete
    if(line_state == "valid" and len(opens) > 0):
        line_state = "incomplete"
    
# Calculate score and display solution
score = 0
for c in corrupted_line_chars:
    score += chunk_values[c]

print("Solution: ", score)
