# input
p1_pos, p2_pos = 8, 4

# sample
#p1_pos, p2_pos = 4, 8
max_points = 10

# A die object
class die:
    def __init__(self, sides):
        self.sides = sides
        self.last_roll = 0
        self.count_rolls = 0

    def deterministic_roll(self):
        self.last_roll = ((self.last_roll)%self.sides) + 1
        self.count_rolls += 1
        return self.last_roll

# A pawn object
class pawn:
    def __init__(self, starting_pos, max_pos):
        self.score = 0
        self.max_pos = max_pos
        self.pos = starting_pos

    def move(self, move):
        self.pos = ((self.pos + move - 1)%self.max_pos) + 1
        self.score += self.pos
        return self.pos

# ---------------------------------------------------------------------------------------------
# ----------------------------------------- MAIN ----------------------------------------------
# ---------------------------------------------------------------------------------------------

# Create a d100 die and 2 pawns
d100 = die(100)
p1 = pawn(p1_pos, max_points)
p2 = pawn(p2_pos, max_points)

# Play Dirac dice
while True:
    roll1 = d100.deterministic_roll()
    roll2 = d100.deterministic_roll()
    roll3 = d100.deterministic_roll()
    print(f"Player 1 rolls: {roll1}+{roll2}+{roll3} and moves to space {p1.move(roll1+roll2+roll3)} for a total score of {p1.score}")
    if p1.score >= 1000: break 

    roll1 = d100.deterministic_roll()
    roll2 = d100.deterministic_roll()
    roll3 = d100.deterministic_roll()
    print(f"Player 2 rolls: {roll1}+{roll2}+{roll3} and moves to space {p2.move(roll1+roll2+roll3)} for a total score of {p2.score}")
    if p2.score >= 1000: break 

print(f"Solution: {min(d100.count_rolls * p1.score, d100.count_rolls * p2.score)}")
