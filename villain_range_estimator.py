from typing import List, Dict
from models.poker_session import PokerSession


class VillainRangeEstimator:
    """
    Naive version: returns a static default range.
    Can be expanded to use VPIP/PFR, position, aggression, etc.
    """

    def __init__(self):
        self.default_range = self._generate_default_range()

    def estimate(self, session: PokerSession) -> List[str]:
        """
        Estimate a villain range based on the session context.

        For now, returns a generic preflop range.
        """
        # TODO: use session.villainProfiles[seatId] in future
        return self.default_range

    def _generate_default_range(self) -> List[str]:
        """
        For now: return top 15% of hands as a list of combos.
        Example combos: 'AhKh', 'TsTd', etc.
        """
        # Simple hardcoded set of good hands for testing
        premium_pairs = ['AA', 'KK', 'QQ', 'JJ', 'TT']
        strong_broadways = ['AKs', 'AQs', 'AJs', 'KQs', 'AKo', 'AQo']
        suited_connectors = ['T9s', '98s']

        combos = []
        for hand in premium_pairs + strong_broadways + suited_connectors:
            combos.extend(self._expand_hand_to_combos(hand))

        return combos

    def _expand_hand_to_combos(self, hand: str) -> List[str]:
        """
        Expand shorthand (e.g. 'AKs') to actual card combinations like 'AhKh', 'AdKd', etc.
        """
        ranks = "AKQJT98765432"
        suits = "shdc"

        def combos_for(suited: bool, offsuit: bool):
            out = []
            for s1 in suits:
                for s2 in suits:
                    if (suited and s1 != s2) or (offsuit and s1 == s2):
                        continue
                    out.append(hand[0] + s1 + hand[1] + s2)
            return out

        if len(hand) == 2:  # pocket pair like 'AA'
            return [hand[0] + s1 + hand[1] + s2 for i, s1 in enumerate(suits) for s2 in suits[i+1:]]

        if hand.endswith('s'):
            return combos_for(suited=True, offsuit=False)
        elif hand.endswith('o'):
            return combos_for(suited=False, offsuit=True)
        else:
            return combos_for(suited=True, offsuit=False) + combos_for(suited=False, offsuit=True)