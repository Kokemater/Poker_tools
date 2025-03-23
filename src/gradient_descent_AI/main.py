
from genetical_ai import *
from evaluate_games import *
import numpy as np
import random


def main():
	#best_model = torch.load("best_model.pth", map_location=TORCH_DEVICE)
	population = []
	for i in range(POPULATION_SIZE):
		model_info = {
			"VPIP": 0, 
			"PFR": 0, 
			"3Bet": 0, 
			"Fold to 3Bet": 0, 
			"Cold Call": 0, 
			"CBet": 0, 
			"Fold to CBet": 0, 
			"Check-Raise": 0, 
			"AF": 0, 
			"Steal": 0, 
			"Fold to Steal": 0, 
			"3-Bet vs Steal": 0, 
			"WTSD": 0, 
			"W$SD": 0, 
			"WWSF": 0, 
			"4-Bet": 0, 
			"Donk Bet": 0, 
			"AFq": 0, 
			"Limp": 0, 
			"Limp-Fold": 0, 
			"Limp-Call": 0, 
			"Limp-Raise": 0
		}
		if i == 0:
			model_info["player_type"] = ["AI", create_individual()]
		else:
			model_info["player_type"] = "random"
		population.append(model_info)

	for gen in range(GENERATIONS):
		scores = simulate_game(population)
		# add SGD

		if gen % 2 == 0:
			print(f"gen {gen} | IA won {scores[1]} chips. ")


if __name__ == "__main__":
	main()