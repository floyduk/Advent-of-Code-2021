# input
p1_pos, p2_pos = 8, 4

# sample
#p1_pos, p2_pos = 4, 8
max_points = 10
max_score = 21

# We roll 3 dice per turn and each roll splits the universe 3 ways. So rolling 1, 1, 1 gives a
# total of 3 and is 1 universe. But a total roll of 4 can happen in 3 universes, a total 5 in 
# 6 universes and so on.
universes_per_die_roll = {3:1, 4:3, 5:6, 6: 7, 7:6, 8:3, 9:1}

# globals tracking wins
p1_win_count, p2_win_count = 0, 0

# Dead simple maths to calculate where the pawn moves to based on given starting pos and die roll
move_pawn = lambda start_pos, move: ((start_pos + move -1)%max_points) + 1

# Recursive function that checks for a win and if nobody has won then kick of 3 new universes
def play_dirac_dice(p1_pos, p1_score, p2_pos, p2_score, count_universes, next_player):
    global p1_win_count, p2_win_count

    if next_player == 1:
        if p2_score >= max_score:
            p2_win_count += count_universes
            if p2_win_count%10000 == 0:
                print(f"p1 wins: {p1_win_count}\t p2 wins: {p2_win_count}")
        else:
            for u in universes_per_die_roll:
                p = move_pawn(p1_pos, u)
                play_dirac_dice(p, p1_score + p, p2_pos, p2_score, count_universes * universes_per_die_roll[u], 2)

    else:
        if p1_score >= max_score:
            p1_win_count += count_universes
            if p1_win_count%10000 == 0:
                print(f"p1 wins: {p1_win_count}\t p2 wins: {p2_win_count}")
        else:
            for u in universes_per_die_roll:
                p = move_pawn(p2_pos, u)
                play_dirac_dice(p1_pos, p1_score, p, p2_score + p, count_universes * universes_per_die_roll[u], 1)


# ---------------------------------------------------------------------------------------------
# ----------------------------------------- MAIN ----------------------------------------------
# ---------------------------------------------------------------------------------------------

# Play Dirac dice 
play_dirac_dice(p1_pos, 0, p2_pos, 0, 1, 1)

print(f"Soltuion: P1 wins {p1_win_count}, P2 wins {p2_win_count}")