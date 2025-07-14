from typing import List, Dict, Optional
from models.board_texture import BoardTexture
from models.hand_context import HandContext


class ClassificationContext:
    def __init__(
        self,
        hero_hand:  List[str],
        board: List[str],
        all_cards: List[str],
        rank_counts: Dict[str, int],
        suit_counts: Dict[str, int],
        hero_ranks: List[str],
        board_ranks: List[str],
        hero_suits: List[str],
        board_suits: List[str],
        hero_values: List[int],
        board_values: List[int],
        all_suits: List[str],
        board_texture: Optional[BoardTexture] = None,
    ):
        self.hero_hand = hero_hand
        self.board = board
        self.all_cards = all_cards
        self.rank_counts = rank_counts
        self.suit_counts = suit_counts
        self.hero_ranks = hero_ranks
        self.board_ranks = board_ranks
        self.hero_suits = hero_suits
        self.board_suits = board_suits
        self.hero_values = hero_values
        self.board_values = board_values
        self.all_suits = all_suits
        self.board_texture = board_texture
        self.highest_board_rank = max(board_values) if board_values else None

    @staticmethod
    def from_hand_context(ctx: HandContext) -> "ClassificationContext":
        return ClassificationContext(
            hero_hand=ctx.hero_hand,
            board=ctx.board,
            all_cards=ctx.all_cards,
            rank_counts=ctx.rank_counts,
            suit_counts=ctx.suit_counts,
            hero_ranks=ctx.hero_ranks,
            board_ranks=ctx.board_ranks,
            hero_suits=ctx.hero_suits,
            board_suits=ctx.board_suits,
            hero_values=ctx.hero_values,
            board_values=ctx.board_values,
            all_suits=ctx.hero_suits + ctx.board_suits,
            board_texture=ctx.board_texture,
        )