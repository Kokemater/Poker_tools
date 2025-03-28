from django.shortcuts import render
import sys
import os

# Aseguramos que la carpeta 'AI' esté en el sys.path antes de intentar importar cualquier módulo.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'principal', 'AI', 'best_model.pth', 'genetical_ai')))
print(sys.path)

# Ahora ya podemos importar el módulo 'solver' desde 'principal.AI'
from principal.AI.solver import solver_map
from principal.AI.genetical_ai import TORCH_DEVICE
import json

table_cards = ["00", "00", "00", "00", "00"]
stack = 100
to_call = 10
n_players_playing = 2
history = []
# /home/jbutragu/poker_tools/src/WEB_SOLVER/poker_solver/templates/poker/solver.html
#map_hands = solver_map(table_cards, stack, to_call, n_players_playing, history)
map_hands = {"as": 2}
# Vista para la página de inicio
def inicio(request):
    map = solver_map(table_cards, stack, to_call, n_players_playing, history)
    print(map)
    return render(request, "solver.html", {"hand_data": json.dumps(map)})

# Vista para la página 'Sobre nosotros'
def sobre(request):
    return render(request, 'sobre.html')
