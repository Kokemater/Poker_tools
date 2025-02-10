import torch

def create_list_starting_from(n):
	return list(range(n, 9)) + list(range(0, n))

def suma_mod9(a, b):
    return (a + b) % 9

def playing(payed, players_playing):
    # Filtrar solo los jugadores que siguen en la mano
    active_payed = payed[players_playing == 1]
    return not torch.all(active_payed == active_payed[0])

        