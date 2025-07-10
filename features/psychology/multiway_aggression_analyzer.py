from typing import Dict

from models.constants import AGGRESSIVE_ACTIONS
from models.villain_action_history import VillainActionHistory


class MultiwayAggressionAnalyzer:
    def __init__(self):
        pass

    def analyze(self, history: VillainActionHistory) -> Dict[str, float]:
        """
        Calculates how often the villain takes aggressive actions in multiway pots.

        Returns:
            {"multiway_aggression_score": float}  # between 0 and 1
        """
        total_multiway_spots = 0
        total_aggressive_actions = 0

        for hand in history.hands:
            all_players = set(a.player for a in hand.actions)
            if len(all_players) < 3:
                continue  # not multiway

            villain_actions = [a for a in hand.actions if a.player == history.seat]
            if not villain_actions:
                continue

            total_multiway_spots += 1
            if any(a.action in AGGRESSIVE_ACTIONS for a in villain_actions):
                total_aggressive_actions += 1

        if total_multiway_spots == 0:
            return {"multiway_aggression_score": 0.0}

        score = total_aggressive_actions / total_multiway_spots
        return {"multiway_aggression_score": round(score, 3)}