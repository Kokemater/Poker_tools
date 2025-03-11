
from genetical_ai import *
from evaluate_games import *
import numpy as np
import random


def main():
	best_model = torch.load("best_model.pth")
	population = [create_individual() for _ in range(POPULATION_SIZE - 1)]
	population.append(best_model)

	for gen in range(GENERATIONS):
		scores = simulate_game(population)
		#print(scores)
		models_with_scores = list(zip(scores, population))
		models_with_scores.sort(reverse=True, key=lambda x: x[0])
		best_scores = [scores for scores, model in models_with_scores[:POPULATION_SIZE // 2]]
		best_models = [model for _, model in models_with_scores[:POPULATION_SIZE // 2]]
		best_model = models_with_scores[0][1]
		new_population = [best_model]  # Mantener al mejor individuo (elitismo)
		for i in range(0, len(best_models) - 1, 2):
			parent1 = best_models[i]
			parent2 = best_models[i + 1]
			child = crossover(parent1, parent2)
			child = mutate(child)
			new_population.append(child)
		new_population = best_models[:]  # Copiar mejores 
		while len(new_population) < POPULATION_SIZE:
			parent1, parent2 = random.choice(best_models), random.choice(best_models)
			child = crossover(parent1, parent2)
			child = mutate(child)
			new_population.append(child)
		population = new_population

		if gen %250 == 0:
			torch.save(best_model, "best_model.pth")
			#print(f"Generación {gen+1} completada.")
			#print(f"Suma de dinero total = {sum(scores)}")

if __name__ == "__main__":
	main()