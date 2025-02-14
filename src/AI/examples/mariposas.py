import torch
import random
import pygame



# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Visualización de scores en Pygame")
pygame.font.init()
font = pygame.font.Font(None, 36)

def show_scores(scores, background_color, generation):
	color = (255 * background_color, 255 * background_color, 255 * background_color)
	screen.fill(color)  # Fondo gris
	for i in range(len(scores)):
		color = int(scores[i] * 255)  # Escalar el color [0,1] -> [0,255]
		pygame.draw.circle(screen, (color, color, color), coords[i], 10)
	
	text_surface = font.render(f"Generación: {generation}", True, (255, 0, 0))  # Texto negro
	screen.blit(text_surface, (20, HEIGHT - 40))
	# Mostrar el número de generación en rojo

	pygame.display.flip()  


N = 10  
MARGIN = 50 
GRID_SIZE = (WIDTH - 2 * MARGIN) // (N - 1) 

# Generar coordenadas para los 100 puntos
coords = [(MARGIN + (i % N) * GRID_SIZE, MARGIN + (i // N) * GRID_SIZE) for i in range(100)]


INPUT_SIZE = 1
HIDDEN_SIZE_1 = 30
HIDDEN_SIZE_2 = 30
OUTPUT_SIZE = 1
POPULATION_SIZE = 100
GENERATIONS = 10000

def sigmoid(x):
	return 1 / (1 + torch.exp(-x))


def create_individual():
	return {
		"W1": torch.randn(INPUT_SIZE, HIDDEN_SIZE_1) * 0.1,
		"b1": torch.randn(HIDDEN_SIZE_1) * 0.1,
		"W2": torch.randn(HIDDEN_SIZE_1, HIDDEN_SIZE_2) * 0.1,
		"b2": torch.randn(HIDDEN_SIZE_2) * 0.1,
		"W3": torch.randn(HIDDEN_SIZE_2, OUTPUT_SIZE) * 0.1,
		"b3": torch.randn(OUTPUT_SIZE) * 0.1
	}

def forward(individual, x):
	x = torch.matmul(x, individual["W1"]) + individual["b1"]
	x = sigmoid(x)
	x = torch.matmul(x, individual["W2"]) + individual["b2"]
	x = sigmoid(x)
	x = torch.matmul(x, individual["W3"]) + individual["b3"]
	return sigmoid(x)

def crossover(parent1, parent2):
	child = create_individual()
	for key in child:
		mask = torch.rand_like(parent1[key]) > 0.5
		child[key] = torch.where(mask, parent1[key], parent2[key])
	return child

def mutate(individual):
	for key in individual:
		if torch.rand(1).item() < 0.1:  # Probabilidad de mutación
			if isinstance(individual[key], torch.Tensor):
				individual[key] += torch.randn_like(individual[key]) * 0.01
	return individual

def simulate_game(population, background_color):
	n_population = len(population)
	scores = torch.zeros(n_population)
	for i in range(n_population):
		x = torch.tensor([background_color], dtype=torch.float32)
		result = forward(population[i], x)
		scores[i] = 1 - abs(background_color - result)
	return scores

def main():
	population = [create_individual() for _ in range(POPULATION_SIZE)]

	for gen in range(GENERATIONS):
		background_color = 0.5 * (1 + torch.sin(torch.tensor(gen * 0.006)))
		scores = simulate_game(population, background_color)
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
		best_color = torch.zeros(len(population))
		x = torch.tensor([background_color], dtype=torch.float32)
		for i in range(len(population)):
			best_color[i] = forward(population[i], x)
		show_scores(best_color, background_color, gen)

		population = new_population
		if gen %100 == 0:
			print(f"Generación {gen+1} completada.")
			print(scores)
	pygame.quit()

if __name__ == "__main__":
	main()
