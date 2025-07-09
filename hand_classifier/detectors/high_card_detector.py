from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength
from utils.poker_utils import int_to_rank


class HighCardDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        all_values = sorted(ctx.hero_values + ctx.board_values, reverse=True)
        high_card_val = all_values[0] if all_values else 0
        high_card_rank = int_to_rank(high_card_val)

        label = f"{high_card_rank} High"
        score = 0.10 if high_card_rank != "A" else 0.20

        return HandStrength(label=label, score=score)