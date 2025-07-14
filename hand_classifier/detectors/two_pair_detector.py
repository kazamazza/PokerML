from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength, HandCategory



class TwoPairDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        # Find all ranks that appear at least twice
        paired_ranks = [rank for rank, count in ctx.rank_counts.items() if count >= 2]

        if len(paired_ranks) >= 2:
            return HandStrength(HandCategory.TWO_PAIR)

        return None