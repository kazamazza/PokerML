from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength, HandCategory


class FlushDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        suit_counts = {s: ctx.all_suits.count(s) for s in set(ctx.all_suits)}
        flush_suit = next((s for s, cnt in suit_counts.items() if cnt >= 5), None)
        if not flush_suit:
            return None

        return HandStrength(HandCategory.FLUSH)