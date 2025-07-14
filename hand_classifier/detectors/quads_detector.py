from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength, HandCategory


class QuadsDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        for rank, count in ctx.rank_counts.items():
            if count == 4:
                return HandStrength(label=HandCategory.QUADS)
        return None