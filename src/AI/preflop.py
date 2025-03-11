DECK  = [
    "2s", "3s", "4s", "5s", "6s", "7s", "8s", "9s", "ts", "js", "qs", "ks", "as",
    "2d", "3d", "4d", "5d", "6d", "7d", "8d", "9d", "td", "jd", "qd", "kd", "ad",
    "2h", "3h", "4h", "5h", "6h", "7h", "8h", "9h", "th", "jh", "qh", "kh", "ah",
    "2c", "3c", "4c", "5c", "6c", "7c", "8c", "9c", "tc", "jc", "qc", "kc", "ac",
]

def is_suited_connector(card1, card2):
    value1, suit1 = card1[0], card1[1]
    value2, suit2 = card2[0], card2[1]
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              't': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}
    if suit1 != suit2:
        return False
    return abs(values[value1] - values[value2]) == 1

def is_pair(card1, card2):
    return card1[0] == card2[0]

def is_broadway(card1, card2):
    broadway_values = {'t', 'j', 'q', 'k', 'a'}
    return card1[0] in broadway_values and card2[0] in broadway_values

def top_card(card1, card2):
    values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
              't': 10, 'j': 11, 'q': 12, 'k': 13, 'a': 14}
    return max(values[card1[0]], values[card2[0]])

def is_good_hand_preflop(card1, card2):
    nuts = 2
    good = 1.5
    middle = 1
    bad = 0

    top = top_card(card1, card2)

    if (is_pair(card1, card2) and top >= 10) or (is_broadway(card1, card2) and top == 14):
        return nuts
    if (is_pair(card1, card2) and top >= 5) or is_broadway(card1, card2):
        return good
    if (is_pair(card1, card2) and top >= 2) or is_suited_connector(card1, card2):
        return middle
    return bad

# Ejemplo de uso
#print(is_good_hand_preflop("as", "ks"))  # 2 (Nuts)
#print(is_good_hand_preflop("9h", "th"))  # 1 (Middle)
#print(is_good_hand_preflop("4c", "4d"))  # 1 (Middle)
#print(is_good_hand_preflop("jc", "qc"))  # 1.5 (Good)
#print(is_good_hand_preflop("2d", "7h"))  # 0 (Bad)
