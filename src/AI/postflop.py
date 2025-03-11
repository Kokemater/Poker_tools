
from combinations import get_rating, get_numeric_rating

def filter_empty_cards(board):
	return [card for card in board if card != "00"]

def classify_board(board):
	"""
	Clasifica el tablero postflop en 'seco' (2), 'húmedo'(0) o 'medio' (1).
	board: Lista de cartas comunitarias, por ejemplo ['2s', '7h', '9d']
	"""
	values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
			  't': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}
	
	board_values = [values[card[0]] for card in board]
	board_suits = [card[1] for card in board]
	
	board_values.sort()

	is_flush_possible = len(set(board_suits)) == 1
	
	is_connected = all(board_values[i] + 1 == board_values[i+1] for i in range(len(board_values) - 1))

	is_semi_connected = False
	for i in range(len(board_values) - 1):
		if board_values[i] + 2 == board_values[i + 1]:  # Hay un gap de una carta
			is_semi_connected = True
			break

	# Detectar si existen cartas altas y cuántas
	high_cards = len([card for card in board_values if card >= 10])

	unique_suits = len(set(board_suits))

	# Evaluar el tipo de tablero
	if is_flush_possible:
		return 0  # Tablero con posibilidad de color
	
	if is_connected:
		return 0  # Tablero con posibilidad de escalera
	
	if is_semi_connected:
		return 1  # Tablero semi-conectado

	# Considerar que si tenemos muchas cartas altas o una combinación de ellas
	if high_cards >= 2:
		return 0  # Dos o más cartas altas (J, Q, K, A) en el tablero
	# Si hay muchos palos únicos, la probabilidad de un color se reduce
	if unique_suits <= 2 and high_cards > 0:
		return 1  # Algunas cartas altas y palos variados
	if unique_suits >= 3:
		return 2  # Si hay demasiados palos diferentes, el tablero es menos probable que sea húmedo
	# Si hay más de dos palos y no hay oportunidades significativas, es seco
	if len(set(board_suits)) > 2 and not is_connected and high_cards == 0:
		return 1  # Cartas que no permiten muchas combinaciones, varios palos
	return 1  # Caso general si no cae en ninguna categoría superior



def get_hand_rating(cards):
	cards = filter_empty_cards(cards)
	rating = get_rating(cards)
	return rating[0] + 0.05*rating[1]

board = ["6s", "6s", "6s", "7h", "9h", "00", "00"]
print(get_hand_rating(board))






################ ################# ##################



# Helper function to evaluate card value
def card_value(card):
	values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
			  't': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}
	return values[card[0].lower()]

# Helper function to get the suit of a card
def card_suit(card):
	return card[1].lower()

# Helper function to filter out empty cards ('00') from the board


# Helper function to count suits in hand and board
def count_suits(hand, board):
	# First filter out empty cards from the board
	board = filter_empty_cards(board)
	suits = [card_suit(card) for card in hand + board]
	return {suit: suits.count(suit) for suit in set(suits)}

# Function to check if there is a flush project (with 4 cards of the same suit on hand and board)
def is_flush_project(hand, board):
	board = filter_empty_cards(board)  # Filter out empty cards
	suit_counts = count_suits(hand, board)
	# If there are 4 or more cards of the same suit, we have a flush project
	return max(suit_counts.values()) == 4

def is_straight_project(hand, board):
	board = filter_empty_cards(board)  
	all_cards= hand + board
	all_cards_n = []
	for card in all_cards:
		all_cards_n.append(card_value(card[0]))
	all_cards_n = sorted(all_cards_n)
	extra_card = 1
	for i in range(len(all_cards_n) - 1):
		if i == 4 and extra_card == 0:
			return True
		if abs(all_cards_n[i] - all_cards_n[i + 1]) == 1:
			continue
		elif abs(all_cards_n[i] - all_cards_n[i + 1]) == 2 and extra_card > 0:
			extra_card = 0
		else:
			return False

	return True
			

def is_straight_project_2_puntas(hand, board):
	board = filter_empty_cards(board)
	values = sorted(set(card_value(card) for card in hand + board))
	if len(values) >= 5:
		# Check if 2-punta straight is possible
		for i in range(len(values) - 4):
			if values[i:i+5] == list(range(values[i], values[i] + 5)):
				return True
	return False

# Function to check if there is a backdoor flush (two suited cards left)
def is_backdoor_flush(hand, board):
	if len(board) == 4:
		return False
	board = filter_empty_cards(board)  # Filter out empty cards
	suits = [card_suit(card) for card in hand + board]
	# If there are two suited cards left in hand+board, it's a backdoor flush
	if suits.count(max(suits, key=suits.count)) == 3:
		return True
	return False

# Function to check if there is a backdoor straight (two more consecutive cards are needed from the remaining deck)
def is_backdoor_straight(hand, board):
	if len(board) == 4:
		return False
	board = filter_empty_cards(board)  
	all_cards= hand + board
	all_cards_n = []
	for card in all_cards:
		all_cards_n.append(card_value(card[0]))
	all_cards_n = sorted(all_cards_n)
	extra_card = 2
	for i in range(len(all_cards_n) - 1):
		if i == 4-1 and extra_card == 1:
			return True
		if i == 3-1 and extra_card == 0:
			return True
		if abs(all_cards_n[i] - all_cards_n[i + 1]) == 1:
			continue
		elif abs(all_cards_n[i] - all_cards_n[i + 1]) <=2 and extra_card > 0:
			extra_card -= 1
		else:
			return False
	return True


def	is_top_pair_avaible(hand, board):
	board = filter_empty_cards(board)  
	my_cards_n = []
	board_cards_n = []
	for card in hand:
		my_cards_n.append(card_value(card[0]))
	for card in board:
		board_cards_n.append(card_value(card[0]))

	if max(my_cards_n) >= max(board_cards_n):
		return True
	return False
# Main function to evaluate hand equity
def hand_equity(hand, board):
	outs = 0  
	board = filter_empty_cards(board)

	if is_top_pair_avaible(hand, board):
		outs += 4
		print("Top pair avaible")
	if is_flush_project(hand, board):
		print("flush project")
		outs += 9
	elif is_backdoor_flush(hand, board):
		print("backdoor flush")
		outs += 2 
	if is_straight_project_2_puntas(hand, board):
		print("straight project 2 ends")
		outs += 8 
	elif is_straight_project(hand, board):
		print("straight project 1 end")
		outs += 4 
	elif is_backdoor_straight(hand, board):
		print("backdoor straight")
		outs += 1

	# Calculate the number of unseen cards
	total_unseen_cards = 5 - len(board)

	# Calculate equity based on the outs and remaining unseen cards
	if (total_unseen_cards == 2):
		equity = outs * 4 / 100
	elif (total_unseen_cards == 1):
		equity = outs * 2 / 100
	else:
		equity = 0
	return equity

# Sample deck of cards (this should be initialized with the full deck)
DECK = [
	"2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "ts", "js", "qs", "ks", "as",
	"2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "td", "jd", "qd", "kd", "ac",
	"2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "th", "jh", "qh", "kh", "ah",
	"2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "tc", "jc", "qc", "kc", "ac",
]

# Example of how to use the functions:

# Sample hand and board (with empty cards '00')
hand = ["8s", "as"]
board = ["6s", "qd", "4h", "00", "00"]  # Two empty cards on the board

# Calculate hand equity
print(f"Board = {board}")
print(f"Hand = {hand}")
equity = hand_equity(hand, board)
print(f"Hand Equity: {equity:.2f}")


def calculate_pot_odds(pot_size, call_size):
	return (call_size/(pot_size + call_size))