import torch
import numpy as np

# Datos de la puerta OR
X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
y = torch.tensor([[0], [1], [1], [1]], dtype=torch.float32)

# Parámetros del algoritmo genético
POPULATION_SIZE = 50  
GENERATIONS = 1000 
MUTATION_RATE = 0.1 

# Definir la estructura de la red neuronal (1 capa oculta con 2 neuronas)
INPUT_SIZE = 2
HIDDEN_SIZE = 2
OUTPUT_SIZE = 1

# Función para crear un individuo (pesos aleatorios)
def create_individual():
    return {
        "W1": torch.randn(INPUT_SIZE, HIDDEN_SIZE),
        "b1": torch.randn(HIDDEN_SIZE),
        "W2": torch.randn(HIDDEN_SIZE, OUTPUT_SIZE),
        "b2": torch.randn(OUTPUT_SIZE),
    }

# Inicializar la población
population = [create_individual() for _ in range(POPULATION_SIZE)]

# Función de activación (sigmoide)
def sigmoid(x):
    return 1 / (1 + torch.exp(-x))

# Función para evaluar un individuo (fitness = precisión en la puerta OR)
def evaluate(individual):
    W1, b1, W2, b2 = individual["W1"], individual["b1"], individual["W2"], individual["b2"]
    hidden = sigmoid(X @ W1 + b1)
    output = sigmoid(hidden @ W2 + b2)
    loss = torch.mean((output - y) ** 2)  # Error cuadrático medio
    return -loss.item()  # Queremos minimizar el error, así que usamos negativo

# Función de selección (elige los mejores individuos)
def select(population):
    population.sort(key=evaluate, reverse=True)
    return population[: POPULATION_SIZE // 2]  # Seleccionamos la mitad mejor

# Función de cruce (crossover) entre dos individuos
def crossover(parent1, parent2):
    child = {}
    for key in parent1:
        mask = torch.rand_like(parent1[key]) > 0.5
        child[key] = torch.where(mask, parent1[key], parent2[key])
    return child

# Función de mutación (ligeros cambios aleatorios en los pesos)
def mutate(individual):
    for key in individual:
        if torch.rand(1).item() < MUTATION_RATE:
            individual[key] += torch.randn_like(individual[key]) * 0.1 
    return individual

# Evolución de la población
for generation in range(GENERATIONS):
    # Evaluar y seleccionar los mejores individuos
    population = select(population)
    
    # Crear nueva generación a partir de los mejores individuos
    new_population = []
    for _ in range(POPULATION_SIZE - len(population)):
        p1, p2 = np.random.choice(population, 2, replace=False)
        child = mutate(crossover(p1, p2))
        new_population.append(child)
    
    # Reemplazar la antigua población con la nueva
    population.extend(new_population)

    # Mostrar la mejor precisión cada 100 generaciones
    if generation % 100 == 0:
        best_fitness = evaluate(population[0])
        ##print(f"Generación {generation}, Mejor Fitness: {best_fitness:.4f}")

# Evaluar el mejor modelo final
best_individual = population[0]
W1, b1, W2, b2 = best_individual["W1"], best_individual["b1"], best_individual["W2"], best_individual["b2"]
hidden = sigmoid(X @ W1 + b1)
final_output = sigmoid(hidden @ W2 + b2)
final_output = final_output.round()  # Redondeamos las salidas a 0 o 1

##print("\nResultados finales:")
##print(final_output)
