from typing import Optional
from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength, HandCategory
from utils.poker_utils import int_to_rank



class HighCardDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        # Always matches as the last fallback
        return HandStrength(HandCategory.HIGH_CARD)