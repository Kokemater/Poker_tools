from postflop import hand_equity, calculate_pot_odds, get_hand_rating
from preflop import is_good_hand_preflop
from genetical_ai import forward, INPUT_SIZE, TORCH_DEVICE
import torch
import random

def random_ai():
	return random.randint(1,3)

def ai(pot_size, call_size, player_cards, board_cards, n_players_playing, player_nn, history):
	pot_odds = calculate_pot_odds(pot_size, call_size)
	equity = hand_equity(player_cards, board_cards)
	preflop_value = is_good_hand_preflop(player_cards[0], player_cards[1])
	hand_rating = get_hand_rating(player_cards + board_cards)
	table_rating = get_hand_rating(["00", "00"] + board_cards)
	n_players = n_players_playing
	x = torch.zeros(INPUT_SIZE, dtype=torch.float32, device=TORCH_DEVICE)
	x[0] = pot_odds
	x[1] = equity
	x[2] = preflop_value
	x[3] = equity
	x[4] = hand_rating
	x[5] = table_rating
	x[6] = n_players
	best_move = forward(player_nn, x)
	return (best_move)

def find_action(pot_size, call_size, player_cards, board_cards, n_players_playing, player, history):
	if player["player_type"] == "random":
		return random_ai()
	if player["player_type"][0] == "AI":
		return ai(pot_size, call_size, player_cards, board_cards, n_players_playing, player["player_type"][1], history)
