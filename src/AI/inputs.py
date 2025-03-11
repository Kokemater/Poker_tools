from postflop import hand_equity, calculate_pot_odds, get_hand_rating
from preflop import is_good_hand_preflop
from genetical_ai import forward, INPUT_SIZE
import torch

def find_best_move(pot_size, call_size, player_cards, board_cards, n_players_playing, player):
	pot_odds = calculate_pot_odds(pot_size, call_size)
	equity = hand_equity(player_cards, board_cards)
	preflop_value = is_good_hand_preflop(player_cards[0], player_cards[1])
	hand_rating = get_hand_rating(player_cards + board_cards)
	n_players = n_players_playing

	x = torch.zeros(INPUT_SIZE, dtype=torch.float32)
	x[0] = pot_odds
	x[1] = equity
	x[2] = preflop_value
	x[3] = equity
	x[4] = hand_rating
	x[5] = n_players
	best_move = forward(player, x)
	return (best_move)







