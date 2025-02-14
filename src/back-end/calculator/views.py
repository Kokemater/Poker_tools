from django.shortcuts import render

import random
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def calculate_equity(request):
    data = request.data  # Recibe los datos enviados desde el frontend
    players = data.get('players', [])
    
    # Generar valores aleatorios de equity
    equities = {f"Jugador {i+1}": round(random.uniform(10, 90), 2) for i in range(len(players))}

    return Response({"equities": equities})

