from genetical_ai import *
import numpy as np
from random import choice
from tools import *
from tabulate import tabulate
from combinations import get_winner
from inputs import find_action


def give_player_cards(deck):
	player_cards = []
	for _ in range(2):
		card = choice(deck)  
		player_cards.append(card)
		deck.remove(card)
	return player_cards

def apply_action(action, player, chips, stack, payed, playing_hand, to_call, to_raise):
	if action == 2 and chips[player] == 0:
		action = 1
	if action == 0:  # Fold
		playing_hand[player] = 0
	elif action == 1:  # Check/Call
		chips[player] -= to_call
		payed[player] += to_call
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
	##print(chips)
	##print(payed)
	return stack

def preflop(stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation,history):
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
			action = find_action(stack, to_call, player_cards[players[i]], table_cards, n_players_playing, poblation[players[i]], history)
			history.append([0, players[i], action])
			#action = input_data(player_cards[players[i]], table_cards, stack, to_call, n_players_playing)
			stack = apply_action(action, players[i], chips, stack, payed, playing_hand, to_call, to_raise)

			n_actions += 1
	return stack

def extract_cards(cards, stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation, deck, history):
	n_actions = 0
	for i in cards:
		table_cards[i] = choice(deck)
		deck.remove(table_cards[i])
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
			#x = input_data(player_cards[players[i]], table_cards, stack, to_call, n_players_playing)
			#stack = take_decission(x, players[i], chips, stack, payed, playing_hand, to_call, to_raise, poblation, player_cards)
			action = find_action(stack, to_call, player_cards[players[i]], table_cards, n_players_playing, poblation[players[i]], history)
			if cards == [0, 1, 2]:
				n = 1
			elif cards == [3]:
				n = 2
			elif cards == [4]:
				n = 3
			else:
				assert("error")
			history.append([n, players[i], action])
			#action = input_data(player_cards[players[i]], table_cards, stack, to_call, n_players_playing)
			stack = apply_action(action, players[i], chips, stack, payed, playing_hand, to_call, to_raise)

			n_actions += 1
		data = [
		["Payout"] + list(payed),
		["Hand"] + list(playing_hand),
		["Chips"] + list(chips)
	]
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
		##print(subpots)
		payed_playing = [x - min_stack if x > 0 else x for x in payed_playing]
	for subpot in (subpots):
		indices = subpots[subpot]
		hands = [hands_playing[i] for i in indices]
		winners = get_winner(table_cards, hands)
		n_winners = len(winners)
		for i in range(n_winners):
			chips[map_index[subpots[subpot][winners[i]]]] += subpot / n_winners

def results_after_hand(game_info):
	game_round, poblation, chips, small_blind, big_blind = game_info
	table_cards = ["00", "00", "00", "00", "00"]
	total_players = len(poblation)
	curr_deck = DECK.copy()
	stack = 0
	playing_hand = torch.ones(total_players, device=TORCH_DEVICE)
	payed = torch.zeros(total_players, device=TORCH_DEVICE)
	sb_position = game_round % total_players
	utg_position = suma_mod(total_players, sb_position, 2)
	players = create_list_starting_from(utg_position, total_players)
	player_cards = [give_player_cards(curr_deck) for _ in range(total_players)]
	stack = blinds(players, chips, payed, stack, small_blind, big_blind)
	history = []
	stack = preflop(stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation,history)
	players = create_list_starting_from(sb_position, total_players)
	stack = extract_cards([0, 1, 2], stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation, curr_deck, history)
	stack = extract_cards([3], stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation, curr_deck, history)
	stack = extract_cards([4], stack, payed, playing_hand, chips, player_cards, table_cards, players, total_players, poblation, curr_deck, history)
	give_stack_to_winner(stack, payed, total_players,chips, playing_hand, player_cards, table_cards, curr_deck)
	return chips

def reload_chips(chips, scores, big_blind):
	for i in range(len(chips)):
		if chips[i] == 0:
			chips[i] = 100 * big_blind
			scores[i] -= 100 * big_blind
