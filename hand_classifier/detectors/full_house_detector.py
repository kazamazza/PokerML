from typing import Optional

from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength


class FullHouseDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        """
        Detects if hero has a full house using combined board + hero cards.
        """
        counts = ctx.rank_counts
        three_of_kind_ranks = [rank for rank, count in counts.items() if count >= 3]
        pair_ranks = [rank for rank, count in counts.items() if count >= 2]

        for trips_rank in three_of_kind_ranks:
            for pair_rank in pair_ranks:
                if trips_rank != pair_rank:
                    return HandStrength(label=f"Full House ({trips_rank} over {pair_rank})", score=0.92)

        # Check for same rank triple + pair (e.g., 9s9h on 9c9d2h)
        if len(three_of_kind_ranks) >= 1 and len(pair_ranks) >= 2:
            trips_rank = three_of_kind_ranks[0]
            pair_rank = [r for r in pair_ranks if r != trips_rank][0]
            return HandStrength(label=f"Full House ({trips_rank} over {pair_rank})", score=0.92)

        return None