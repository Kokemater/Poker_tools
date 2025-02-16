from genetical_ai import *
import numpy as np
from random import choice
from tools import *
from tabulate import tabulate
from combinations import get_winner


def input_data():
    x = torch.zeros(1, 9)
	
def one_hot_card(card):
	if card[0] == "0":
		return torch.zeros(17)
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

DECK  = [
    "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "ts", "js", "qs", "ks", "as",
    "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "td", "jd", "qd", "kd", "ac",
    "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "th", "jh", "qh", "kh", "ah",
    "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "tc", "jc", "qc", "kc", "ac",
]

def give_player_cards(deck):
	player_cards = []
	for _ in range(2):
		card = choice(deck)  
		player_cards.append(card)
		deck.remove(card)
	return player_cards

def input_data(player_cards, table_cards, stack, to_call, n_players_playing):
    x = torch.zeros(INPUT_SIZE, dtype=torch.float32)
    
    # Cartas del jugador (2 cartas)
    x[0:17] = one_hot_card(player_cards[0])
    x[17:34] = one_hot_card(player_cards[1])

    # Cartas de la mesa (hasta 5 cartas)
    if len(table_cards) >= 1:
        x[34:51] = one_hot_card(table_cards[0])
    if len(table_cards) >= 2:
        x[51:68] = one_hot_card(table_cards[1])
    if len(table_cards) >= 3:
        x[68:85] = one_hot_card(table_cards[2])
    if len(table_cards) >= 4:
        x[85:102] = one_hot_card(table_cards[3])
    if len(table_cards) >= 5:
        x[102:119] = one_hot_card(table_cards[4])

    x[119] = float(stack)
    x[120] = float(to_call)
    x[121] = float(n_players_playing)
    return x

def take_decission(x, player, chips, stack, payed, playing_hand, to_call, to_raise, poblation, player_cards):
	action = forward(poblation[player], x)
	if action == 2 and chips[player] == 0:
		action = 1
	if action == 0:  # Fold
		#print(f" Player {player} fold : {player_cards[player]}")
		playing_hand[player] = 0
	elif action == 1:  # Check/Call
		#print("!!!!!!!!!!1")
		#print(to_call)
		chips[player] -= to_call
		payed[player] += to_call
		#print(to_call)
		#print("!!!!!!!!!!1")
		stack += to_call

	elif action >= 2:  # Raise (100% del bote)
		payed[player] += to_raise
		chips[player] -= to_raise
		stack += to_raise
	return stack
		
def	blinds(players, chips, payed, stack, small_blind, big_blind):
	# Pequeña ciega
	if small_blind > chips[players[-2]]:
		small_blind = chips[players[-2]]
	if big_blind > chips[players[-1]]:
		big_blind = chips[players[-1]]
	chips[players[-2]] -= small_blind
	payed[players[-2]] += small_blind
	stack += small_blind
	# Ciega grande
	chips[players[-1]] -= big_blind
	payed[players[-1]] += big_blind
	stack += big_blind
	#print(chips)
	#print(payed)
	return stack

def preflop(stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation):
	n_actions = 0
	while playing(payed, playing_hand, chips, n_actions):
		for i in range(total_players):
			if not playing(payed, playing_hand,chips, n_actions):
				break
			if not playing_hand[players[i]] or chips[players[i]] == 0:
				n_actions += 1
				continue
			n_players_playing = torch.count_nonzero(playing_hand == 1).item()
			to_call = payed.max().item() - payed[players[i]].item()
			if to_call > chips[players[i]]:
				to_call = chips[players[i]].item()
			to_raise = stack
			if stack > chips[players[i]]:
				to_raise = chips[players[i]].item()
			x = input_data(player_cards[players[i]], table_cards, stack, to_call, n_players_playing)
			stack = take_decission(x, players[i], chips, stack, payed, playing_hand, to_call, to_raise, poblation, player_cards)
			n_actions += 1
	data = [
		["Payout"] + list(payed),
		["Hand"] + list(playing_hand),
		["Chips"] + list(chips)
	]
	#print("---------------PREFLOP TERMINADO----------------")
	#print(tabulate(data, tablefmt="grid"))
	return stack

def extract_cards(cards, stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation, deck):
	n_actions = 0
	for i in cards:
		table_cards[i] = choice(deck)
		deck.remove(table_cards[i])
	#print(table_cards)
	first_move = True
	while first_move or playing(payed, playing_hand, chips, n_actions):
		first_move = False
		for i in range(total_players):
			if not playing(payed, playing_hand, chips, n_actions):
				break
			if not playing_hand[players[i]]  or chips[players[i]] == 0:
				n_actions += 1
				continue
			n_players_playing = torch.count_nonzero(playing_hand == 1).item()
			to_call = min(payed.max().item() - payed[players[i]].item(), chips[players[i]])
			to_raise = stack
			if stack > chips[players[i]]:
				to_raise = chips[players[i]].item()
			x = input_data(player_cards[players[i]], table_cards, stack, to_call, n_players_playing)
			stack = take_decission(x, players[i], chips, stack, payed, playing_hand, to_call, to_raise, poblation, player_cards)
			n_actions += 1
		data = [
		["Payout"] + list(payed),
		["Hand"] + list(playing_hand),
		["Chips"] + list(chips)
	]
	#print("---------------RONDA TERMINADA----------------")
	#print(tabulate(data, tablefmt="grid"))
	return stack

def give_stack_to_winner(stack, payed, total_players, chips, playing_hand, player_cards, table_cards, deck):
	hands_playing = []
	payed_playing = []

	n_hands_playing = 0
	map_index: dict[int, int] = {}

	for i in range(total_players):
		if playing_hand[i] == 1:
			hands_playing.append(player_cards[i]) 
			payed_playing.append(payed[i])
			map_index[n_hands_playing] = i
			n_hands_playing += 1

	subpots = {}
	previous_stack = sum(payed[playing_hand == 0])
	while not all(x <= 0 for x in payed_playing):  
		n_players_in_stack = sum(x > 0 for x in payed_playing)
		min_stack = min([x for x in payed_playing if x > 0])
		total_pot = n_players_in_stack * min_stack
		if len(subpots) == 0:
			total_pot += previous_stack
		subpots[total_pot] = []
		for i in range(n_hands_playing):
			if payed_playing[i] > 0:
				subpots[total_pot].append(i)
		#print(subpots)
		payed_playing = [x - min_stack if x > 0 else x for x in payed_playing]
	for subpot in (subpots):
		indices = subpots[subpot]
		hands = [hands_playing[i] for i in indices]
		winners = get_winner(table_cards, hands)
		#print("------")
		#print("subpot: ")
		#print(subpot)
		#print("indices")
		#print(indices)
		#print("winners")
		n_winners = len(winners)
		for i in range(n_winners):
			#print(subpots[subpot][winners[i]])
			chips[map_index[subpots[subpot][winners[i]]]] += subpot / n_winners

def results_after_hand(game_round, poblation, chips, small_blind, big_blind):
	table_cards = ["00", "00", "00", "00", "00"]
	total_players = len(poblation)
	curr_deck = DECK.copy()
	stack = 0
	playing_hand = torch.ones(total_players)
	payed = torch.zeros(total_players)
	sb_position = game_round % total_players
	utg_position = suma_mod9(sb_position, 2)
	players = create_list_starting_from(utg_position)
	player_cards = [give_player_cards(curr_deck) for _ in range(total_players)]
	stack = blinds(players, chips, payed, stack, small_blind, big_blind)
	stack = preflop(stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation)
	players = create_list_starting_from(sb_position)
	stack = extract_cards([0, 1, 2], stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation, curr_deck)
	stack = extract_cards([3], stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation, curr_deck)
	stack = extract_cards([4], stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation, curr_deck)
	give_stack_to_winner(stack, payed, total_players,chips, playing_hand, player_cards, table_cards, curr_deck)
	return chips

def reload_chips(chips, scores, big_blind):
	for i in range(len(chips)):
		if chips[i] == 0:
			chips[i] = 100 * big_blind
			scores[i] -= 100 * big_blind

def simulate_game(poblation):
	small_blind = 5
	big_blind = 10
	n_games = 100
	scores = torch.zeros(len(poblation))
	for round in range(n_games):
		chips = torch.ones(len(poblation)) * (100 * big_blind)
		chips = results_after_hand(round, poblation, chips, small_blind, big_blind)
		scores += chips
		scores -= (100 *big_blind)
	return scores