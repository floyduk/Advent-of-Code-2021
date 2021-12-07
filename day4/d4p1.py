import fileinput

class bingo_card:
        def __init__(self):
            self.numbers = list()
            self.width = 0
            self.bingo = False

        def already_won(self):
            return(self.bingo)

        def add_row(self, line):
            self.numbers.extend(line.split())
            if(self.width == 0):            # The first line of numbers sets the width of this board
                self.width = len(self.numbers)

        def print_board(self):
            print("Board width: ", self.width)
            print("Board numbers: ",self.numbers)

        def call_number(self, n):
            if(n in self.numbers):
                i = self.numbers.index(n)
                self.numbers[i] = "x"
                return(self.check_for_win(i))
            else:
                return(False)

        def index_to_coordinates(self, i):
            y = i // self.width             # // is integer division
            x = i % self.width
            return((x, y))

        def coordinates_to_index(self, x, y):
            return((y*self.width) + x)

        def is_marked(self, x, y):
            return(self.numbers[self.coordinates_to_index(x, y)] == "x")

        def check_for_win(self, i):
            (x, y) = self.index_to_coordinates(i)

            # Check row
            count_marks = 0
            for a in range(0, self.width):
                count_marks += 1 if self.is_marked(a, y) else 0
            if(count_marks == self.width):
                self.bingo = True
                return(True)

            # Check column
            height = len(self.numbers) // self.width
            count_marks = 0
            for a in range(0, height):
                count_marks += 1 if self.is_marked(x, a) else 0
            if(count_marks == height):
                self.bingo = True
                return(True)

            return(False)

        def sum_of_unmarked_numbers(self):
            total = 0
            for n in self.numbers:
                if(n != "x"):
                    total += int(n)
            return(total)

# Declare an empty list that will soon contain bingo card objects
bingo_cards = list()

# Read in bingo boards until we run out of input - there is no error handling here
|for line in fileinput.input():
    line = line.rstrip()

    if("," in line):                        # if the line contains a comma then it's the called numbers list
        called_numbers = line.split(",")
    elif(line == ""):                       # If we find a blank line then create a new bingo card
        bingo_cards.append(bingo_card())
    else:                                   # else add the data to the current bingo card
        bingo_cards[-1].add_row(line)

# Start calling numbers
number_of_cards = len(bingo_cards)
number_of_wins = 0
for n in called_numbers:
    for card in bingo_cards:
        if(not card.already_won()):         # Don't bother playing cards that have already won
            if(card.call_number(n)):        # This returns true if we have a winner
                number_of_wins += 1
                if(number_of_wins == 1):
                    print("FIRST WIN", number_of_wins)
                    print("Winning number: ", n)
                    print("Sum of unmarked numbers: ", card.sum_of_unmarked_numbers())
                    print("Solution:", card.sum_of_unmarked_numbers() * int(n))
                elif(number_of_wins == number_of_cards):
                    print("LAST WIN", number_of_wins)
                    print("Winning number: ", n)
                    print("Sum of unmarked numbers: ", card.sum_of_unmarked_numbers())
                    print("Solution:", card.sum_of_unmarked_numbers() * int(n))
                    exit()
