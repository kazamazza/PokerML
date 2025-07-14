from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength, HandCategory


class OnePairDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        pair_ranks = [r for r, c in ctx.rank_counts.items() if c == 2]
        if pair_ranks:
            return HandStrength(HandCategory.ONE_PAIR)
        return None