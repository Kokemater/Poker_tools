def card_value(card):
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


def get_pairs(table, player):
    joined = table + player
    pairs = []
    for i in range(len(joined)):
        for j in range(i + 1, len(joined)):
            if joined[i][0] == joined[j][0]:
                if not card_value(joined[i]) in pairs:
                    pairs.append(card_value(joined[i]))
    return pairs


def get_three(table, player):
    joined = table + player
    a = [0 for _ in range(14)]
    ret = []
    for v in joined:
        a[card_value(v)] += 1
    for v in a:
        if v == 3:
            ret.append(v)
    return ret


def get_straight(table, player):
    joined = sorted(table + player, key=lambda c: card_value(c))
    starts = []
    for i in range(len(joined) - 5 + 1):
        last = card_value(joined[i])
        is_straight = True
        for j in range(i + 1, i + 5):
            if (card_value(joined[j]) != last + 1 and
                    not (card_value(joined[j]) == 2 and last == 14)):
                is_straight = False
                break
            last = card_value(joined[j])
        if is_straight:
            starts.append(card_value(joined[i]))
    return starts


def _is_color(cards):
    col = cards[0][1]
    for c in cards:
        if c[1] != col:
            return False
    return True


def has_color(table, player):
    joined = sorted(table + player, key=lambda c: color_key(c))
    for i in range(len(joined) - 5):
        if _is_color(joined[i:i+5]):
            return True
    return False


def get_high_card(table, player):
    return max([card_value(c) for c in player])


table = ["4s", "5d", "ks", "jh", "6c"]
player = ["2s", "3s"]

print(get_pairs(table, player))
print(get_high_card(table, player))
print(get_three(table, player))
print(get_straight(table, player))
print(has_color(table, player))
