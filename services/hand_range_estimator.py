from typing import List, Dict, Any

from models.game_round import GameRound
from services.hand_ranges.postflop_range_generator import PostflopRangeGenerator
from services.hand_ranges.preflop_range_provider import PreflopRangeProvider
from services.hand_ranges.range_adjuster import RangeAdjuster

class HandRangeEstimator:
    def __init__(self):
        self.preflop_provider = PreflopRangeProvider()
        self.adjuster = RangeAdjuster()
        self.postflop_generator = PostflopRangeGenerator()

    def generate_preflop(self) -> List[Dict[str, Any]]:
        output = []
        for role in self.preflop_provider.supported_roles():
            for villain_type in self.adjuster.weights.keys():
                base = self.preflop_provider.get_range(role)
                weighted = self.adjuster.apply(base, villain_type)
                output.append({
                    "player_role": role,
                    "round": GameRound.Preflop,
                    "villain_type": villain_type,
                    "hand_range": weighted
                })
        return output

    def generate_postflop(self) -> List[Dict[str, Any]]:
        return self.postflop_generator.generate_ranges()

    def generate_all(self) -> List[Dict[str, Any]]:
        return self.generate_preflop() + self.generate_postflop()