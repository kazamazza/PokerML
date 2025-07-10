from typing import List, Dict, Set

from services.hand_ranges.board_texture_loader import BoardTextureLoader
from services.hand_ranges.postflop_range_refiner import PostflopRangeRefiner
from services.hand_ranges.preflop_range_provider import PreflopRangeProvider
from services.hand_ranges.villain_range_adjuster import VillainRangeAdjuster


class PostflopRangeGenerator:
    def __init__(self):
        self.preflop_provider = PreflopRangeProvider()
        self.refiner = PostflopRangeRefiner()
        self.adjuster = VillainRangeAdjuster()
        self.board_textures = BoardTextureLoader.load()

        self.villain_types = [
            "tight", "loose", "aggressive", "passive", "maniac", "calling-station"
        ]

    def generate_ranges(self) -> List[Dict]:
        results = []
        inserted_keys: Set[str] = set()

        for player_role in self.preflop_provider.supported_roles():
            for round in ["flop", "turn", "river"]:
                for cluster_key, board_list in self.board_textures.items():
                    for board in board_list:
                        board_cards = board.split(",")
                        base_range = self.refiner.refine(
                            self.preflop_provider.get_range(player_role),
                            board_cards
                        )

                        for villain_type in self.villain_types:
                            unique_key = f"{player_role}-{round}-{cluster_key}-{villain_type}"
                            if unique_key in inserted_keys:
                                continue
                            inserted_keys.add(unique_key)

                            weighted_range = self.adjuster.apply_weights(
                                base_range,
                                villain_type
                            )

                            if not weighted_range:
                                weighted_range = [
                                    {"hand": "AA", "weight": 1.0},
                                    {"hand": "KK", "weight": 1.0},
                                    {"hand": "QQ", "weight": 1.0},
                                    {"hand": "AKs", "weight": 1.0},
                                    {"hand": "AQs", "weight": 1.0},
                                    {"hand": "KQs", "weight": 1.0},
                                ]

                            results.append({
                                "player_role": player_role,
                                "round": round,
                                "board_cluster": cluster_key,
                                "board": board,
                                "villain_type": villain_type,
                                "hand_range": weighted_range
                            })

        print(f"✅ Generated {len(results)} postflop ranges.")
        return results