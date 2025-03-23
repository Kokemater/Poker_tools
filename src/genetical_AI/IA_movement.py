from genetical_ai import forward, TORCH_DEVICE
import torch
from inputs import find_action

def main():
	best_model = torch.load("best_model.pth", map_location=TORCH_DEVICE)
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
