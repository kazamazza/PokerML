from typing import Optional

from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength


class TripsDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        for rank, count in ctx.rank_counts.items():
            if count == 3:
                # Make sure it's not a pocket pair (SetDetector should handle that)
                if rank in ctx.board_ranks and rank in ctx.hero_ranks:
                    label = f"Trips ({rank})"
                    return HandStrength(label=label, score=0.57)
        return None