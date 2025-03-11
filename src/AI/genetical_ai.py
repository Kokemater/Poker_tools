import torch
import torch.nn.functional as F

INPUT_SIZE = 7
HIDDEN_SIZE_1 = INPUT_SIZE*16
HIDDEN_SIZE_2 = INPUT_SIZE*16
OUTPUT_SIZE = 3
POPULATION_SIZE = 6
GENERATIONS = 1000

TORCH_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Red Neuronal (función de activación y forward)
def sigmoid(x):
    return 1 / (1 + torch.exp(-x))
def create_individual():
    """Crea una red neuronal con pesos inicializados aleatoriamente"""
    return {
        "W1": torch.randn(INPUT_SIZE, HIDDEN_SIZE_1, device=TORCH_DEVICE) * 0.1,
        "b1": torch.randn(HIDDEN_SIZE_1, device=TORCH_DEVICE) * 0.1,
        "W2": torch.randn(HIDDEN_SIZE_1, HIDDEN_SIZE_2, device=TORCH_DEVICE) * 0.1,
        "b2": torch.randn(HIDDEN_SIZE_2, device=TORCH_DEVICE) * 0.1,
        "W3": torch.randn(HIDDEN_SIZE_2, OUTPUT_SIZE, device=TORCH_DEVICE) * 0.1,
        "b3": torch.randn(OUTPUT_SIZE, device=TORCH_DEVICE) * 0.1
    }

def forward(individual, x):
    x = torch.matmul(x, individual["W1"]) + individual["b1"]
    x = sigmoid(x)
    x = torch.matmul(x, individual["W2"]) + individual["b2"]
    x = sigmoid(x)
    x = torch.matmul(x, individual["W3"]) + individual["b3"]
    action = torch.argmax(F.softmax(x, dim=0))  # Devuelve el índice de la máxima probabilidad
    return action.item()

# Algoritmo Genético
def crossover(parent1, parent2):
    child = create_individual()  # Crear un nuevo niño
    for key in child:
        if torch.rand(1, device=TORCH_DEVICE).item() > 0.5:
            child[key] = parent1[key]
        else:
            child[key] = parent2[key]
    return child

def mutate(individual):
    for key in individual:
        if torch.rand(1, device=TORCH_DEVICE).item() < 0.8:  # Tasa de mutación
            individual[key] += torch.randn_like(individual[key], device=TORCH_DEVICE) * 2  # Perturba los pesos
    return individual
