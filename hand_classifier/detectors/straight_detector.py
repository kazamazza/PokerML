from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength, HandCategory

class StraightDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        all_values = sorted(set(ctx.hero_values + ctx.board_values))
        if len(all_values) < 5:
            return None

        # Ace‐low wheel support
        if 14 in all_values:
            all_values.insert(0, 1)

        # Look for any five‐card run
        for i in range(len(all_values) - 4):
            window = all_values[i : i + 5]
            if window[4] - window[0] == 4:
                return HandStrength(HandCategory.STRAIGHT)

        return None