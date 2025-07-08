from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass

@dataclass
class FeatureExtractor:
    """
    Extracts ML-ready features from a parsed poker hand record.
    """

    def extract(self, hand: Dict, street: str) -> Optional[Tuple[Dict, str]]:
        if not hand.get("hero") or not hand.get("hero_hand"):
            return None

        try:
            features = {
                "street": street,
                "hero_hand": self.encode_hand(hand["hero_hand"]),
                "spr": self.compute_spr(hand),
                "in_position": self.compute_in_position(hand),
                "num_players": self.count_players(hand),
                "board_texture": self.analyze_board_texture(hand.get("board", [])),
                "action_history": self.simplify_action_history(
                    hand.get("actions") or hand.get("action_line", ""), hand["hero"]
                ),
            }

            label = self.extract_label_from_action_line(hand)
            return features, label

        except Exception as e:
            print(f"❌ Failed to extract features for hand {hand.get('hand_id')}: {e}")
            return None

    # ── Label Extraction ──────────────────────────────────────

    def extract_label_from_action_line(self, hand: Dict) -> str:
        line = hand.get("action_line", "").lower()

        if "folds" in line:
            return "fold"
        elif "calls" in line:
            return "call"
        elif "raises" in line:
            return "raise"
        elif "bets" in line:
            return "bet"
        elif "checks" in line:
            return "check"
        return "unknown"

    # ── Feature Functions ──────────────────────────────────────

    def encode_hand(self, cards: List[str]) -> str:
        return ''.join(cards)

    def compute_spr(self, hand: Dict) -> float:
        stack = hand.get("stack", 100)
        pot = hand.get("pot", 10)
        return round(stack / pot, 2) if pot else 0.0

    def compute_in_position(self, hand: Dict) -> int:
        return 1 if hand.get("in_position", False) else 0

    def count_players(self, hand: Dict) -> int:
        return len(hand.get("villains", [])) + 1

    def analyze_board_texture(self, board: List[str]) -> str:
        if not board:
            return "empty"

        suits = [card[1] for card in board]
        unique_suits = len(set(suits))

        if unique_suits == 1:
            return "monotone"
        elif unique_suits == 2:
            return "two-tone"
        else:
            return "rainbow"

    def simplify_action_history(self, raw_actions: Union[List[str], str], hero: str) -> str:
        if isinstance(raw_actions, str):
            raw_actions = [raw_actions]

        history = []
        for line in raw_actions:
            line = line.lower()
            if "folds" in line:
                history.append("F")
            elif "calls" in line:
                history.append("C")
            elif "raises" in line or "bets" in line:
                history.append("R")
            elif "checks" in line:
                history.append("X")

        return ''.join(history[-10:])