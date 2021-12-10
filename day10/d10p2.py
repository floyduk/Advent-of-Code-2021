import fileinput

chunk_openers = ["(", "[", "{", "<"]
chunk_closers = [")", "]", "}", ">"]
autocomplete_values = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

# Read the file line by line
autocomplete_scores = list()
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
                line_state = "corrupted"
                break
            else:
                # Closing a chunk
                del(opens[-1])

    # If we reach here without the line being corrupted but we have remaining opens then it is incomplete
    if(line_state == "valid" and len(opens) > 0):
        # Complete the line by popping the last item off the opens list until the list is empty
        score = 0
        while(len(opens) > 0):
            # Figure out what character is required to close the next chunk
            required_closer = chunk_closers[chunk_openers.index(opens[-1])]
            line.append(required_closer)    # I don't actually *need* to do this. Nobody is checking the lines.
            del opens[-1]

            # Keep track of the score for this line
            score = score * 5
            score += autocomplete_values[required_closer]

        # Add the total score for this line to the list of autocomplete_scores
        autocomplete_scores.append(score)

# Sort the autocomplete scores and then find the median value
autocomplete_scores = sorted(autocomplete_scores)
median = autocomplete_scores[int(len(autocomplete_scores)/2)]
print(f"Solution: {median}")
