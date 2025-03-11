def card_value(card):
    if len(card) == 0:
        return 0
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
    if len(card) == 0:
        return 0
    if card[1] == 's':
        return 1
    if card[1] == 'd':
        return 2
    if card[1] == 'c':
        return 3
    if card[1] == 'h':
        return 4


def is_straight(cards):
    last = cards[0]
    for i in range(1, len(cards)):
        if cards[i] != last - 1 or cards[i] == 0:
            return False
        last = cards[i]
    return True


def get_straight(cards):
    cards = sorted(list(set([card_value(c) for c in cards])), reverse=True)
    if len(cards) < 5:
        return False
    for i in range(len(cards) - 5 + 1):
        if is_straight(cards[i:i+5]):
            return cards[i]
    return False


def get_colors(cards):
    cards = sorted(cards, key=lambda c: color_key(c))
    colors = [
        sorted([c for c in cards if c[1] == 's'],
               key=lambda c: card_value(c), reverse=True),
        sorted([c for c in cards if c[1] == 'h'],
               key=lambda c: card_value(c), reverse=True),
        sorted([c for c in cards if c[1] == 'd'],
               key=lambda c: card_value(c), reverse=True),
        sorted([c for c in cards if c[1] == 'c'],
               key=lambda c: card_value(c), reverse=True),
    ]
    ret = [c for c in colors if len(c) >= 5]
    return ret[0] if len(ret) > 0 else False


def get_best_color(colors):
    return [card_value(c) for c in colors[:5]]


EVAL_HIGH = 1
EVAL_PAIRS = 2
EVAL_DPAIRS = 3
EVAL_SET = 4
EVAL_STRAIGHT = 5
EVAL_FLUSH = 6
EVAL_FULL = 7
EVAL_POKER = 8
EVAL_STRAIGHT_FLUSH = 9


def get_poker(cards):
    cards = sorted(cards, key=lambda c: card_value(c), reverse=True)
    poker = get_first_repeated(cards, 4)
    if poker is False:
        return False
    cards = [card_value(c) for c in cards if card_value(c) != poker]
    return [poker, cards[0]]


def get_highs(cards):
    return sorted([card_value(c) for c in cards], reverse=True)[:5]


def get_first_repeated(cards, repeat_count):
    count = 0
    last = cards[0] if len(cards) > 0 else ""
    rep = 0
    for c in cards:
        if card_value(c) == card_value(last):
            count += 1
        else:
            count = 1
        if count == repeat_count:
            rep = card_value(c)
            break
        last = c
    if rep == 0:
        return False
    return rep


def get_pair(cards):
    cards = sorted(cards, key=lambda c: card_value(c), reverse=True)
    pair = get_first_repeated(cards, 2)
    if pair is False:
        return False
    cards = [card_value(c) for c in cards if card_value(c) != pair]
    return [pair] + cards[:3]


def get_dpair(cards):
    cards = sorted(cards, key=lambda c: card_value(c), reverse=True)
    pair1 = get_first_repeated(cards, 2)
    if pair1 is False:
        return False
    cards = [c for c in cards if card_value(c) != pair1]
    pair2 = get_first_repeated(cards, 2)
    if pair2 is False:
        return False
    cards = [c for c in cards if card_value(c) != pair2]
    return [pair1, pair2, card_value(cards[0]) if len(cards) != 0 else 0]


def get_set(cards):
    cards = sorted(cards, key=lambda c: card_value(c), reverse=True)
    st = get_first_repeated(cards, 3)
    if st is False:
        return False
    cards = [card_value(c) for c in cards if card_value(c) != st]
    return [st] + cards[:2]


def get_full_house(cards):
    cards = sorted(cards, key=lambda c: card_value(c), reverse=True)
    st = get_first_repeated(cards, 3)
    if st is False:
        return False
    cards = [c for c in cards if card_value(c) != st]
    pair = get_first_repeated(cards, 2)
    if pair is False:
        return False
    return [st, pair]


def get_rating(cards):
    #print(cards)
    colors = get_colors(cards)
    if colors is not False:
        straight = get_straight(colors)
        if straight is not False:
            return (EVAL_STRAIGHT_FLUSH, straight)
    poker = get_poker(cards)
    if poker is not False:
        return tuple([EVAL_POKER] + poker)
    full = get_full_house(cards)
    if full is not False:
        return tuple([EVAL_FULL] + full)
    if colors is not False:
        best_color = get_best_color(colors)
        return tuple([EVAL_FLUSH] + best_color)
    straight = get_straight(cards)
    if straight is not False:
        return (EVAL_STRAIGHT, straight)
    trio = get_set(cards)
    if trio is not False:
        return tuple([EVAL_SET] + trio)
    dpair = get_dpair(cards)
    if dpair is not False:
        return tuple([EVAL_DPAIRS] + dpair)
    pair = get_pair(cards)
    if pair is not False:
        return tuple([EVAL_DPAIRS] + pair)
    return tuple([EVAL_HIGH] + get_highs(cards))


def get_numeric_rating(rating):
    sum = 0
    for i in range(len(rating)):
        sum += rating[i] * 14 ** (5 - i)
    return sum


def get_winner(table, players):
    ratings = [get_numeric_rating(get_rating(table + p)) for p in players]
    m = max(ratings)
    return [i for i, r in enumerate(ratings) if r == m]



cards = ['2s', '3s', '4s', '5s', '6s']
#print(get_rating(cards))