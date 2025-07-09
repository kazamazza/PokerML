from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength


class QuadsDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        for rank, count in ctx.rank_counts.items():
            if count == 4:
                label = f"Quads ({rank})"
                return HandStrength(label=label, score=0.95)
        return None