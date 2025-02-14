def card_value(card):
    if card[0] == 't':
        return 10
    if card[0] == 'j':
        return 11
    if card[0] == 'q':
        return 12
    if card[0] == 'k':
        return 13
    if card[0] == 'a':
        return 14
    return int(card[0])


def color_key(card):
    if card[1] == 's':
        return 1
    if card[1] == 'd':
        return 2
    if card[1] == 'c':
        return 3
    if card[1] == 'h':
        return 4


def get_equal(cards, amount):
    cards = [card_value(c) for c in cards]
    pairs = []
    counts = {}
    for v in cards:
        if v in counts:
            counts[v] += 1
        else:
            counts[v] = 1
    for v, c in counts.items():
        n = c // amount
        # for i in range(n):
        if n > 0:
            pairs.append(v)
    return pairs


def _is_straight_r(cards):
    cards = sorted([card_value(c) for c in cards], reverse=True)
    last = cards[0]
    for i in range(1, len(cards)):
        if cards[i] != last - 1:
            return False
        last = cards[i]
    return True


def _is_straight(cards):
    last = cards[0]
    for i in range(1, len(cards)):
        if cards[i] != last - 1:
            return False
        last = cards[i]
    return True


def get_straight(cards):
    cards = sorted(list(set([card_value(c) for c in cards])), reverse=True)
    if len(cards) < 5:
        return False
    for i in range(len(cards) - 5 + 1):
        if _is_straight(cards[i:i+5]):
            return cards[i:i+5]
    return False


def _is_color(cards):
    col = cards[0][1]
    for c in cards:
        if c[1] != col:
            return False
    return col


def get_colors(cards):
    cards = sorted(cards, key=lambda c: color_key(c))
    colors = []
    for i in range(len(cards) - 5):
        col = _is_color(cards[i:i+5])
        if col is not False:
            colors.append(cards[i:i+5])
    return colors


def has_color(cards):
    cards = sorted(cards, key=lambda c: color_key(c))
    for i in range(len(cards) - 5):
        col = _is_color(cards[i:i+5])
        if col is not False:
            return col
    return False


def get_highs(cards):
    return sorted([card_value(c) for c in cards], reverse=True)[:5]


def get_high_card(table, player):
    return max([card_value(c) for c in player])


def is_full_house(threes, pairs):
    for p in pairs:
        if threes[0] != p:
            return [threes[0], p]
    return False


# table = ["5s", "6s", "7s", "5h", "4c"]
# player = ["4s", "3s"]
# table = ["kd", "3d", "4s", "5h", "4c"]
# player1 = ["4s", "3s"]
# player2 = ["4s", "4s"]

BOT_HIGH = 0
TOP_HIGH = BOT_HIGH + 14 * 5
BOT_PAIRS = (TOP_HIGH + 1) * 2
TOP_PAIRS = BOT_PAIRS + 14 * 3
BOT_THREES = (TOP_PAIRS + 1) * 2
TOP_THREES = BOT_THREES + 14 * 2
BOT_STRAIGHT = (TOP_THREES + 1) * 2
TOP_STRAIGHT = BOT_STRAIGHT + 14
BOT_FLUSH = (TOP_STRAIGHT + 1) * 2
TOP_FLUSH = BOT_FLUSH + 1
BOT_FULL = (TOP_FLUSH + 1) * 2
TOP_FULL = BOT_FULL + 1
BOT_POKER = (TOP_FULL + 1) * 2
TOP_POKER = BOT_POKER + 1
BOT_STRAIGHT_FLUSH = (TOP_POKER + 1) * 2
TOP_STRAIGHT_FLUSH = BOT_STRAIGHT_FLUSH + 1


def evaluate_cards(cards):
    pairs = get_equal(cards, 2)
    threes = get_equal(cards, 3)
    poker = get_equal(cards, 4)
    high_cards = get_highs(cards)
    straight = get_straight(cards)
    colors = get_colors(cards)
    eval = 0

    for c in colors:
        if _is_straight_r(c):
            eval += BOT_STRAIGHT_FLUSH
            # print("flush straight")
    if len(poker) > 0:
        eval += BOT_POKER
        # print(poker[0], "poker")
    fh = is_full_house(pairs, threes)
    if fh is not False:
        eval += BOT_FULL
        # print(fh, "full house")
    if len(colors) > 0:
        eval += BOT_FLUSH
        # print(colors, "color")
    if straight is not False:
        # print(straight, "straight")
        eval += BOT_STRAIGHT + straight[0]
    if len(threes) > 0:
        eval += BOT_THREES + sum(threes)
        # print(threes, "threes")
    if len(pairs) > 1:
        eval += BOT_PAIRS + sum(pairs)
        # print(pairs, "double pairs")
    elif len(pairs) > 0:
        eval += BOT_PAIRS + sum(pairs)
        # print(pairs, "pair")
    eval += BOT_HIGH + sum(high_cards)
    # print(high_cards, "high cards")
    return eval


def get_winner(table, player1, player2):
    p1e = evaluate_cards(table + player1)
    p2e = evaluate_cards(table + player2)
    if p1e == p2e:
        return -1
    if p1e > p2e:
        return 0
    return 1


# print(get_winner(table, player1, player2))
