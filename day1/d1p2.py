import fileinput

count_increases = 0
val=[-1,-1,-1]
for line in fileinput.input():
        lasttotal = sum(val)
        del val[0]
        val.append(int(line))
        thistotal = sum(val)

        if not -1 in val:
                if thistotal > lasttotal:
                        print("increase ", lasttotal, " < ", thistotal)
                        count_increases += 1

print("total count increases: ", count_increases)
