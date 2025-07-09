from typing import Dict
from models.villain_action_history import VillainActionHistory


class ShowdownStatsAnalyzer:
    def analyze(self, history: VillainActionHistory) -> Dict[str, float]:
        total_hands = len(history.hands)
        hands_to_showdown = 0

        for hand in history.hands:
            if hand.get("showdown", False):
                hands_to_showdown += 1

        return {
            "showdown_percentage": hands_to_showdown / total_hands if total_hands else 0.0
        }