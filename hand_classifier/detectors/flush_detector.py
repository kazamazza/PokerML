from typing import Optional

from hand_classifier.classification_context import ClassificationContext
from models.hand_strength import HandStrength
from utils.poker_utils import rank_to_int, int_to_rank


class FlushDetector:
    def detect(self, ctx: ClassificationContext) -> Optional[HandStrength]:
        # Count suits among all cards
        suit_counts = {suit: ctx.all_suits.count(suit) for suit in set(ctx.all_suits)}

        # Check for flush (5+ cards of the same suit)
        flush_suit = next((suit for suit, count in suit_counts.items() if count >= 5), None)
        if not flush_suit:
            return None

        # Extract all cards of the flush suit
        suited_cards = [card for card in ctx.all_cards if card[-1] == flush_suit]
        suited_ranks = sorted([rank_to_int(card[:-1]) for card in suited_cards], reverse=True)

        high_card = suited_ranks[0]
        label = f"Flush (High {int_to_rank(high_card)})"
        score = 0.82  # Can be tuned based on strength buckets

        return HandStrength(label=label, score=score)