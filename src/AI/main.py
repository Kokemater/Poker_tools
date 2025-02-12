
from genetical_ai import *
from simulate_game import *
import numpy as np

# Input : 
# Player_card1, Player_card2
# Board_card1, Board_card2, Board_card3, Board_card4, Board_card5
# Call_size
# Pot_size
# N_players_behind

# Output :
# Fold - Check/Fold - Raise

INPUT_SIZE = 2*17 + 5*17 + 1 + 1 + 1
HIDDEN_SIZE_1 = 8
HIDDEN_SIZE_2 = 8
OUTPUT_SIZE = 3
POPULATION_SIZE = 9 
GENERATIONS = 100 

def main():
	# Crear población inicial
	population = [create_individual(INPUT_SIZE, HIDDEN_SIZE_1, HIDDEN_SIZE_2, OUTPUT_SIZE) for _ in range(POPULATION_SIZE)]

	# Entrenamiento por generaciones
	for gen in range(GENERATIONS):
		scores = simulate_game(population)
		models_with_scores = list(zip(scores, population))
		models_with_scores.sort(reverse=True, key=lambda x: x[0])
		best_models = [model for _, model in models_with_scores[:POPULATION_SIZE // 2]]
		new_population = []
		for i in range(0, len(best_models) - 1, 2):
			parent1 = best_models[i]
			parent2 = best_models[i+1]
			child = crossover(parent1, parent2)
			child = mutate(child)
			new_population.append(child)

		# Si hay un número impar de mejores modelos, agregamos el último modelo sin cruces
		if len(best_models) % 2 != 0:
			new_population.append(best_models[0])
		population = new_population
		print(f"Generación {gen+1} completada.")


if __name__ == "__main__":
	main()