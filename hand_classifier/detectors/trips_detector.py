from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength, HandCategory


class TripsDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        # Determine if hero holds a pocket pair
        has_pocket_pair = (ctx.hero_ranks[0] == ctx.hero_ranks[1])
        pocket_rank = ctx.hero_ranks[0] if has_pocket_pair else None

        for rank, count in ctx.rank_counts.items():
            if count == 3:
                # Skip pocket sets (handled by SetDetector)
                if has_pocket_pair and rank == pocket_rank:
                    continue
                # Any other three‐of‐a‐kind is Trips
                return HandStrength(HandCategory.TRIPS)
        return None