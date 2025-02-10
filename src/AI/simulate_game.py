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
    "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "ts", "js", "qs", "ks", "as",
    "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "td", "jd", "qd", "kd", "ac",
    "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "th", "jh", "qh", "kh", "ah",
    "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "tc", "jc", "qc", "kc", "ac",
]

def give_player_cards():
	player_cards = []
	for _ in range(2):
		card = choice(deck)  
		player_cards.append(card)
		deck.remove(card)
	return player_cards


def simulate_game(poblation, input_size):
	small_blind = 5
	big_blind = 10
	n_games = 100
	chips = torch.ones(len(poblation)) * 1000
	total_players = len(poblation)

	for round in range(n_games):
		stack = 0
		playing_hand = torch.ones(total_players)
		payed = torch.zeros(len(poblation))
		sb_position = round % total_players
		utg_position = suma_mod9(sb_position, 2)
		players = create_list_starting_from(utg_position)
		current_deck = deck[:]
		player_cards = [give_player_cards() for _ in range(total_players)]
		
		# Pequeña ciega
		chips[players[-2]] -= small_blind
		payed[players[-2]] += small_blind
		stack += small_blind
		
		# Ciega grande
		chips[players[-1]] -= big_blind
		payed[players[-1]] += big_blind
		stack += big_blind
		
		while playing(payed, playing_hand):
			for i in range(total_players):
				if not playing_hand[players[i]]:
					continue
				n_players_playing = torch.count_nonzero(playing_hand == 1).item()
				to_call = max(payed.max().item() - payed[players[i]].item(), 0)
				x = torch.zeros(input_size, dtype=torch.float32)
				x[0:17] = one_hot_card(player_cards[i][0])
				x[17:34] = one_hot_card(player_cards[i][1])
				x[-3] = float(stack)
				x[-2] = float(to_call)
				x[-1] = int(n_players_playing)
				print("----")
				print(payed)
				print(playing_hand)
				print(chips)
				action = forward(poblation[players[i]], x)
				if action == 2 and chips[players[i]] == 0:
					action = 1
				if action == 0:  # Fold
					playing_hand[players[i]] = 0
					payed[players[i]] = 0
				elif action == 1:  # Check/Call
					if chips[players[i]] >= to_call:
						chips[players[i]] -= to_call
						payed[players[i]] = payed.max()
						stack += to_call
					else:
						payed[players[i]] = chips[players[i]]
						chips[players[i]] = 0
				elif action >= 2:  # Raise (100% del bote)
					raise_value = min(stack, chips[players[i]])
					chips[players[i]] -= raise_value
					payed[players[i]] += raise_value
					stack += raise_value
		print("---------------PREFLOP TERMINADO----------------")
		print(payed, stack, playing_hand)



