from typing import List

RANK_ORDER = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
              '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11,
              'Q': 12, 'K': 13, 'A': 14}

def get_rank_value(rank: str) -> int:
    """Alias for rank_to_int (explicitly used in some modules)."""
    return RANK_ORDER.get(rank.upper(), 0)

def rank_to_int(rank: str) -> int:
    """Standardized rank to integer conversion."""
    return RANK_ORDER.get(rank.upper(), 0)

def int_to_rank(value: int) -> str:
    inverse = {v: k for k, v in RANK_ORDER.items()}
    return inverse.get(value, "?")

def parse_cards(card_str: str) -> List[str]:
    """Split a raw string like 'AhKd' into ['Ah', 'Kd']."""
    return [card_str[i:i+2] for i in range(0, len(card_str), 2)]

def flatten_cards(card_list: List[str]) -> str:
    """Convert a list like ['Ah', 'Kd'] back to 'AhKd'."""
    return ''.join(card_list)