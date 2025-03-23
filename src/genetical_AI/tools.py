import torch

def create_list_starting_from(n, n_players):
	return list(range(n, n_players)) + list(range(0, n))

def suma_mod(mod ,a, b):
    return (a + b) % mod

def all_negative(list):
	for i in list:
		if i > 0:
			return False
	return True

def playing(payed, players_playing, chips, n_actions):
	n_players = len(payed)
	active_payed = payed[players_playing == 1]
	active_chips = chips[players_playing == 1]

	if len(active_payed) == 1:
		return False
	max_payed = torch.max(active_payed)
	if torch.all(active_payed == max_payed) and n_actions >= n_players:
		return False  # Se cierra la ronda

	for i in range(len(active_payed)):
		if active_payed[i] < max_payed and active_chips[i] > 0:
			return True  # Aún hay jugadores que deben igualar la apuesta
	if n_actions >= n_players:
		return False
	else:
		return True