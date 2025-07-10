from dataclasses import dataclass, field
from typing import List, Optional, Dict, Counter
from models.board_texture import BoardTexture
from utils.poker_utils import rank_to_int


@dataclass
class HandContext:
    hero_hand: str                                # e.g. "AhKs"
    board: List[str]                              # e.g. ["Ad", "7c", "2h"]
    board_texture: Optional[BoardTexture]         # From BoardAnalyzer
    all_cards: List[str] = field(init=False)      # Hero + board
    hero_cards: List[str] = field(init=False)     # ["Ah", "Ks"]
    all_ranks: List[str] = field(init=False)      # ["A", "K", "A", "7", "2"]
    all_values: List[int] = field(init=False)     # [14, 13, 14, 7, 2]
    suit_counts: Dict[str, int] = field(init=False)  # e.g. {'h': 2, 'c': 1, 'd': 2}
    rank_counts: Dict[str, int] = field(init=False)  # e.g. {'A': 2, 'K': 1, '7': 1, '2': 1}

    hero_ranks: List[str] = field(init=False)     # ["A", "K"]
    board_ranks: List[str] = field(init=False)    # ["A", "7", "2"]
    hero_suits: List[str] = field(init=False)     # ["h", "s"]
    board_suits: List[str] = field(init=False)    # ["d", "c", "h"]
    hero_values: List[int] = field(init=False)    # [14, 13]
    board_values: List[int] = field(init=False)   # [14, 7, 2]

    def __post_init__(self):
        self.hero_cards = [self.hero_hand[:2], self.hero_hand[2:]]
        self.all_cards = self.hero_cards + self.board

        self.hero_ranks = [c[:-1] for c in self.hero_cards]
        self.board_ranks = [c[:-1] for c in self.board]
        self.all_ranks = self.hero_ranks + self.board_ranks

        self.hero_suits = [c[-1] for c in self.hero_cards]
        self.board_suits = [c[-1] for c in self.board]
        self.suit_counts = Counter(self.hero_suits + self.board_suits)

        self.rank_counts = Counter(self.all_ranks)

        self.hero_values = sorted([rank_to_int(r) for r in self.hero_ranks], reverse=True)
        self.board_values = sorted([rank_to_int(r) for r in self.board_ranks], reverse=True)
        self.all_values = self.hero_values + self.board_values