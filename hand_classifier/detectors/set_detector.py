from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength, HandCategory


class SetDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        # Must be a pocket pair
        if ctx.hero_ranks[0] != ctx.hero_ranks[1]:
            return None

        pocket_rank = ctx.hero_ranks[0]
        # Check for exactly three of that rank across hand+board
        if ctx.rank_counts.get(pocket_rank, 0) == 3:
            return HandStrength(HandCategory.SET)

        return None