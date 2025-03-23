import torch
import torch.nn.functional as F

INPUT_SIZE = 7
HIDDEN_SIZE_1 = INPUT_SIZE*16
HIDDEN_SIZE_2 = INPUT_SIZE*16
OUTPUT_SIZE = 3
POPULATION_SIZE = 6
GENERATIONS = 30000

TORCH_DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

DECK = [
    "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "ts", "js", "qs", "ks", "as",
    "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "td", "jd", "qd", "kd", "ad",
    "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "th", "jh", "qh", "kh", "ah",
    "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "tc", "jc", "qc", "kc", "ac"
]

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

