from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength


class ComboDrawDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        flush_draw = self._detect_flush_draw(ctx)
        straight_draw = self._detect_straight_draw(ctx)

        if flush_draw and straight_draw:
            return HandStrength(label="Combo Draw", score=0.55)
        return None

    def _detect_flush_draw(self, ctx: ClassificationContext) -> bool:
        suit_counts = {s: ctx.all_suits.count(s) for s in set(ctx.all_suits)}
        return any(count == 4 for count in suit_counts.values())

    def _detect_straight_draw(self, ctx: ClassificationContext) -> bool:
        all_values = sorted(set(ctx.hero_values + ctx.board_values))
        if 14 in all_values:
            all_values.insert(0, 1)
        for i in range(len(all_values) - 3):
            if all_values[i + 3] - all_values[i] <= 4:
                return True
        return False