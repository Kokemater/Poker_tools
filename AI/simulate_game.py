from genetical_ai import *
import numpy as np
from random import choice
from tools import *

def input_data():
    x = torch.zeros(1, 9)
	
def one_hot_card(card):
    valor_vec = torch.zeros(13)  # 13 valores: [2, 3, ..., A]
    palo_vec = torch.zeros(4)    # 4 palos: [♥, ♦, ♣, ♠]
    value = card[0]
    suit = card[1]
    map_value = {"2" : 0, "3" : 1, "4": 2, "5": 3, "6": 4, "7": 5, "8" : 6, "9": 7, "t": 8, "j": 9, "q": 10, "k" : 11, "a": 12}
    map_suit = {"h" : 0, "d" : 1, "c": 2, "s": 3}
    valor_vec[map_value[value]] = 1
    palo_vec[map_suit[suit]] = 1
    return torch.cat([valor_vec, palo_vec])  # Concatenar en un solo vector

def winner(a, b):
    # Aquí deberías implementar una lógica para determinar al ganador
    return 1  # Esto está solo como ejemplo

deck  = [
    "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "js", "qs", "ks", "as",
    "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "jd", "qd", "kd", "ac",
    "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "jh", "qh", "kh", "ah",
    "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "jc", "qc", "kc", "ac",
]

def give_player_cards():
	player_cards = []
	for _ in range(2):
		card = choice(deck)  
		player_cards.append(card)
		deck.remove(card)
	return player_cards


def simulate_game(poblation):
	small_blind = 5
	big_blind = 10
	n_games = 100
	chips = torch.ones(1, len(poblation))*1000
	playing_hand = torch.ones(1, len(poblation))
	x = torch.zeros(1, len(poblation))
	for round in range(n_games):
		stack = 0
		to_call = torch.zeros(1, len(poblation))
		sb_position = round % 9
		utg_position = suma_mod9(sb_position, 2)
		players = create_list_starting_from(utg_position)
		chips[players[0]] -= small_blind
		stack += small_blind
		chips[players[1]] -= big_blind
		stack += big_blind
		for i in range(9):
			if not playing_hand[players[i]]:
				continue
			player_cards = give_player_cards()
			x[0, 0:6] = one_hot_card(player_cards[0]) # First player card
			x[0, 7:13] = one_hot_card(player_cards[1]) # Second player card
			x[0, -1] = 9 - i
			x[0, -2] = stack
			x[0, -3] = to_call
			action = forward(poblation[i], x)
			if action == 0: # fold
				playing_hand[1, i] = 0
			if action == 1: # Check/ Call
				chips[i] -= to_call 
			if action >= 2: # Raise (100% pot)
				to_call = stack
				player_cards -= stack


		

