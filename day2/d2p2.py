import fileinput

aim = 0
depth = 0
x = 0
for line in fileinput.input():
        [command, parameter] = line.split()
        parameter = int(parameter)

        print(f"{command}:{parameter}")

        if command == "forward":
                depth += aim * parameter
                x += parameter
        elif command == "up":
                aim -= parameter
        elif command == "down":
                aim += parameter
        else:
                print("unknown command found: ", command)

        print ("-aim: ", aim, " x: ", x, " depth:", depth)

print("aim: ", aim, " x: ", x, " depth: ", depth, " solution: ", (depth*x))
