import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))  # Agregar raíz del proyecto

import torch
from principal.AI.genetical_ai import TORCH_DEVICE
from principal.AI.inputs import find_action
from itertools import product

def generate_poker_hands():
    ranks = ["a", "k", "q", "j", "t", "9", "8", "7", "6", "5", "4", "3", "2"]
    suits = ["s", "h", "d", "c"]
    hands = []
    
    for i, rank1 in enumerate(ranks):
        for j, rank2 in enumerate(ranks):
            hand_name = rank1 + rank2 + ("s" if i < j else "o" if i > j else "")
            combs = []
            for suit1, suit2 in product(suits, repeat=2):
                if "o" in hand_name and suit1 == suit2:
                    continue  # Evitar suited en off-suited
                if "s" in hand_name and suit1 != suit2:
                    continue  # Evitar off-suited en suited
                if not ("o" in hand_name or "s" in hand_name) and suits.index(suit2) <= suits.index(suit1):
                    continue  # Evitar duplicados en parejas
                combs.append(f"{rank1}{suit1}_{rank2}{suit2}")
            hands.extend(combs)
    return hands


def solver_map(table_cards, stack, to_call, n_players_playing, history):
	best_model = torch.load("principal/AI/best_model.pth", map_location=TORCH_DEVICE)
	map_hands = {}
	all_combinations = generate_poker_hands()
	for player_cards in all_combinations:
		cards = player_cards.split('_')
		print(cards)
		action = find_action(stack, to_call, cards, table_cards, n_players_playing, best_model, history)
		map_hands[player_cards] = action
	return(map_hands)
"""
table_cards = ["00", "00", "00", "00", "00"]
stack = 100
to_call = 10
n_players_playing = 2
history = []
map_hands = solver_map(table_cards, stack, to_call, n_players_playing, history)

print(map_hands)
"""

