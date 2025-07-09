from typing import Optional

from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength


class TwoPairDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        # Find all ranks that appear at least twice across hand + board
        paired_ranks = [rank for rank, count in ctx.rank_counts.items() if count >= 2]

        if len(paired_ranks) >= 2:
            # Optional: sort by strength for a cleaner label
            sorted_pairs = sorted(paired_ranks, key=lambda r: ctx.rank_to_int[r], reverse=True)
            label = f"Two Pair ({sorted_pairs[0]} & {sorted_pairs[1]})"
            return HandStrength(label=label, score=0.52)

        return None