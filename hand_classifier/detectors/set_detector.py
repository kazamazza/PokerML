from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength


class SetDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        # Pocket pair in hand?
        if ctx.hero_ranks[0] != ctx.hero_ranks[1]:
            return None

        pocket_rank = ctx.hero_ranks[0]
        if ctx.rank_counts.get(pocket_rank, 0) == 3:
            board_values = ctx.board_values
            hero_value = ctx.hero_values[0]
            top_board = board_values[0] if board_values else 0

            if hero_value == top_board:
                return HandStrength("Top Set", 0.65)
            elif hero_value >= sorted(board_values)[1]:
                return HandStrength("Middle Set", 0.60)
            else:
                return HandStrength("Bottom Set", 0.57)

        return None