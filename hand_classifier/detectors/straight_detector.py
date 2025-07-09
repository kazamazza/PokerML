from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength
from utils.poker_utils import int_to_rank


class StraightDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        all_values = sorted(set(ctx.hero_values + ctx.board_values))
        if len(all_values) < 5:
            return None

        # Append Ace as 1 for wheel detection
        if 14 in all_values:
            all_values.insert(0, 1)

        for i in range(len(all_values) - 4):
            window = all_values[i:i + 5]
            if window[4] - window[0] == 4:
                high_card = window[4]
                label = f"Straight (High {int_to_rank(high_card)})"
                return HandStrength(label=label, score=0.75)

        return None