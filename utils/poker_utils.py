RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
              '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11,
              'Q': 12, 'K': 13, 'A': 14}

def rank_to_int(rank: str) -> int:
    return RANK_ORDER.get(rank.upper(), 0)

def int_to_rank(value: int) -> str:
    inverse = {v: k for k, v in RANK_ORDER.items()}
    return inverse.get(value, "?")