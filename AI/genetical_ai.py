import torch


# Red Neuronal (función de activación y forward)
def sigmoid(x):
    return 1 / (1 + torch.exp(-x))
def create_individual(input_size, hidden_size_1, hidden_size_2, output_size):
    """Crea una red neuronal con pesos inicializados aleatoriamente"""
    return {
        "W1": torch.randn(input_size, hidden_size_1) * 0.1,
        "b1": torch.randn(hidden_size_1) * 0.1,
        "W2": torch.randn(hidden_size_1, hidden_size_2) * 0.1,
        "b2": torch.randn(hidden_size_2) * 0.1,
        "W3": torch.randn(hidden_size_2, output_size) * 0.1,
        "b3": torch.randn(output_size) * 0.1
    }

def forward(individual, x):
    x = torch.matmul(x, individual["W1"]) + individual["b1"]
    x = sigmoid(x)
    x = torch.matmul(x, individual["W2"]) + individual["b2"]
    x = sigmoid(x)
    x = torch.matmul(x, individual["W3"]) + individual["b3"]
    return x


# Algoritmo Genético
def crossover(parent1, parent2):
    child = create_individual()  # Crear un nuevo niño
    for key in child:
        if torch.rand(1).item() > 0.5:
            child[key] = parent1[key]
        else:
            child[key] = parent2[key]
    return child

def mutate(individual):
    for key in individual:
        if torch.rand(1).item() < 0.1:  # Tasa de mutación
            individual[key] += torch.randn_like(individual[key]) * 0.01  # Perturba los pesos
    return individual