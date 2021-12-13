import fileinput

depth = 0
x = 0
for line in fileinput.input():
        wordlist = line.split()
        command = wordlist[0]
        parameter = int(wordlist[1])

        if command == "forward":
                x += parameter
        elif command == "up":
                depth -= parameter
        elif command == "down":
                depth += parameter
        else:
                print("unknown command found: ", command)

print("x: ", x, " depth: ", depth, " solution: ", (depth*x))