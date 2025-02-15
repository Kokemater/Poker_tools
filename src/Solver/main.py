from random import choice
from combinations import get_winner

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "t", "j", "q", "k", "a"]
colors = ["s", "d", "h", "c"]
deck = [r + c for c in colors for r in ranks]


def known_equity(table, players):
    avail_deck = [c for c in deck if c not in table +
                  [it for sublist in players for it in sublist]]
    wins = [0 for p in players]
    runs = 100000
    ties = 0
    for i in range(runs):
        new_table = table.copy()
        new_avail_deck = avail_deck.copy()
        for i in range(5 - len(new_table)):
            new_table.append(choice(new_avail_deck))
            new_avail_deck = [c for c in new_avail_deck if c not in new_table]
        winner = get_winner(new_table, players)
        if len(winner) == 1:
            wins[winner[0]] += 1
        if len(winner) > 1:
            ties += 1
    return [w / runs for w in wins] + [ties / runs]


print(known_equity(["2s", "3s", "5s"], [["2h", "3h"], ["5d", "7h"]]))
