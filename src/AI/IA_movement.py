from genetical_ai import forward
import torch
from inputs import find_action
"""
DECK  = [
    "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "ts", "js", "qs", "ks", "as",
    "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "td", "jd", "qd", "kd", "ac",
    "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "th", "jh", "qh", "kh", "ah",
    "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "tc", "jc", "qc", "kc", "ac",
]
"""
def main():
	best_model = torch.load("best_model.pth")
	player_cards = input("Player cards: ").split() # 2s 3s
	table_cards = input("Table cards: ").split() # as th 9h 00 00
	stack = int(input("stack: "))
	to_call = int(input("Chips to call: ")) # 0 if no chips to call
	n_players_playing = int(input("n_players_playing: "))
	action = find_action(stack, to_call, player_cards, table_cards, n_players_playing, best_model)

	if action == 0:  # Fold
		print(f"AI says FOLD")
	elif action == 1: # Check/Call 
		if to_call == 0:
			print(f"AI says CHECK")
		else:
			print(f"AI says CALL")
	elif action >= 2:  # Raise (100% del bote)
			print(f"AI says RAISE {stack} chips")

main()