from simulate_game_tools import *

def simulate_game(poblation):
	small_blind = 5
	big_blind = 10
	n_games = 100
	scores = torch.zeros(len(poblation))
	chips = torch.ones(len(poblation)) * (100 * big_blind)
	round = 0
	game_info = [round, poblation, chips, small_blind, big_blind]
	for game_info[0] in range(n_games):
		game_info[2] = torch.ones(len(poblation)) * (100 * big_blind)
		game_info[2] = results_after_hand(game_info)
		scores += game_info[2]
		scores -= (100 *big_blind)
	return scores