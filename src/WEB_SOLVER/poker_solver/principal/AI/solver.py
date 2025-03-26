from genetical_ai import forward, TORCH_DEVICE, DECK
import torch
from inputs import find_action
import itertools


def solver_map(table_cards, stack, to_call, n_players_playing, history):
	best_model = torch.load("best_model.pth", map_location=TORCH_DEVICE)
	map_hands = {}
	all_combinations = list(itertools.combinations(DECK, 2))
	for player_cards in all_combinations:
		action = find_action(stack, to_call, list(player_cards), table_cards, n_players_playing, best_model, history)
		map_hands[player_cards] = action
	return(map_hands)





