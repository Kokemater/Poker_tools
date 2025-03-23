import torch
import torch.nn as nn
import numpy as np
import random

# 1️⃣ Definir la red neuronal simple (jugador)
class NeuralNetwork(nn.Module):
    def __init__(self, input_size=2, hidden_size=8, output_size=1):
        super().__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, output_size)
    
    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.sigmoid(self.fc2(x))  # Probabilidad de ganar
        return x

# 2️⃣ Inicializar población de redes neuronales
def create_population(size):
    return [NeuralNetwork() for _ in range(size)]

# 3️⃣ Función de evaluación: juega un juego simple y asigna puntuaciones
def evaluate(network):
    """Simula un juego y devuelve una puntuación para la IA."""
    wins = 0
    for _ in range(10):  # Jugar 10 partidas
        input_data = torch.rand(2)  # Simulación de un estado del juego
        prediction = network(input_data)
        if prediction > 0.5:  # Si predice > 0.5, gana la partida
            wins += 1
    return wins

# 4️⃣ Selección: Elegimos los mejores jugadores
def select_best(population, num_best=4):
    scores = [(net, evaluate(net)) for net in population]
    scores.sort(key=lambda x: x[1], reverse=True)  # Ordenar por puntuación
    return [net for net, _ in scores[:num_best]]

# 5️⃣ Crossover: Cruzar redes neuronales
def crossover(parent1, parent2):
    child = NeuralNetwork()
    for param1, param2, child_param in zip(parent1.parameters(), parent2.parameters(), child.parameters()):
        mask = torch.rand_like(param1) > 0.5  # 50% de genes de cada padre
        child_param.data = torch.where(mask, param1.data, param2.data)
    return child

# 6️⃣ Mutación: Introducir cambios aleatorios
def mutate(network, mutation_rate=0.1):
    for param in network.parameters():
        if torch.rand(1).item() < mutation_rate:  # Probabilidad de mutación
            param.data += torch.randn_like(param) * 0.1  # Pequeño cambio
    return network

# 7️⃣ Algoritmo Genético: Evolucionar la IA
def genetic_algorithm(num_generations=20, population_size=10):
    population = create_population(population_size)

    for generation in range(num_generations):
        ##print(f"\n🧬 Generación {generation + 1}")

        # Seleccionar los mejores jugadores
        best_players = select_best(population)

        # Cruzar y mutar para generar nueva población
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(best_players, 2)
            child = crossover(parent1, parent2)
            child = mutate(child)
            new_population.append(child)

        population = new_population  # Reemplazar con la nueva generación

        # Mostrar el mejor puntaje
        best_score = max(evaluate(net) for net in best_players)
        ##print(f"🔹 Mejor puntuación: {best_score}/10")

# Ejecutar la evolución
genetic_algorithm()
