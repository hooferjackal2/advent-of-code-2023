import re

def score(hand, part):
    card_vals = {'A': 14, 'K': 13, 'Q': 12, 'J': 11 if part == 1 else 0,'T': 10,'9': 9,
                 '8': 8, '7': 7, '6': 6, '5': 5, '4': 4, '3': 3, '2': 2}
    best_hand = hand
    if part == 2 and hand != 'JJJJJ': best_hand = hand.replace('J', max(set(hand.replace('J','')), key=hand.count))
    return sorted([best_hand.count(c) for c in set(best_hand)], reverse=True) + [card_vals[c] for c in hand]


def solve(filename, part):
    with open('input') as f: handbids = [re.findall('\w+', line) for line in f.readlines()]
    handbids.sort(key=lambda x: score(x[0], part))
    return sum([(i+1) * int(hb[1]) for i, hb in enumerate(handbids)])


print(solve('input', 1))
print(solve('input', 2))