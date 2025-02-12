import numpy as np
from random import randint, choice

def winner(a, b):
    # Aquí deberías implementar una lógica para determinar al ganador
    return 1  # Esto está solo como ejemplo

deck  = [
    "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "10s", "js", "qs", "ks", "as",
    "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "10d", "jd", "qd", "kd", "ac",
    "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "10h", "jh", "qh", "kh", "ah",
    "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "10c", "jc", "qc", "kc", "ac",
]

def main():
    # Set player cards
    n_players = int(input("players: "))
    player_cards = []
    for i in range(n_players):
        player = input(f"player {i+1} : ").split()
        player_cards.append(player)
    
    # Set table cards
    table_cards = input("Table cards: ").split()
    n_table_cards = len(table_cards)

    # Error checking
    if n_table_cards not in [0, 3, 4, 5]:
        print("Error : This is not a real situation")
        return

    # Delete these cards from deck
    for i in range(n_players):
        for j in range(len(player_cards[i])):
            card = player_cards[i][j]
            if card in deck:
                deck.remove(card)
    for card in table_cards:
        deck.remove(card)

    # Simulate games
    n_games = 10
    wins = np.zeros(n_players)

    for i in range(n_games):
        current_deck = deck.copy()  
        current_table_cards = table_cards.copy()

        while len(current_table_cards) < 5:
            card = choice(current_deck)  
            current_table_cards.append(card)
            current_deck.remove(card)

        wins[winner(current_table_cards, player_cards)] += 1

    for i in range(n_players):
        print(f"Player {i+1} equity: {wins[i]/n_games * 100} %")

main()
