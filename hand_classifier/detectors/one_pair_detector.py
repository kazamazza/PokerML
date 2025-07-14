from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength
from utils.poker_utils import RANK_ORDER


class OnePairDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        pair_ranks = [rank for rank, count in ctx.rank_counts.items() if count == 2]

        if pair_ranks:
            highest_pair = max(pair_ranks, key=lambda r: RANK_ORDER[r])
            is_top_pair = RANK_ORDER[highest_pair] == ctx.highest_board_rank
            pair_type = "Top Pair" if is_top_pair else "One Pair"
            score = 0.47 if is_top_pair else 0.36

            return HandStrength(label=f"{pair_type} ({highest_pair})", score=score)

        return None