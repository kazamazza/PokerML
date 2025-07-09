from typing import Dict

from models.villain_action_history import VillainActionHistory


class AggressionStatsAnalyzer:
    def analyze(self, history: VillainActionHistory) -> Dict[str, float]:
        total_bets = 0
        total_raises = 0
        total_calls = 0
        total_check_raises = 0
        total_check_opportunities = 0

        for hand in history.hands:
            for street in ["flop", "turn", "river"]:
                actions = hand.get(street, [])
                previous_action = None

                for i, action in enumerate(actions):
                    if action["player"] != "villain":
                        continue

                    if action["type"] == "bet":
                        total_bets += 1
                    elif action["type"] == "raise":
                        total_raises += 1
                    elif action["type"] == "call":
                        total_calls += 1
                    elif action["type"] == "raise" and previous_action and previous_action["type"] == "check":
                        total_check_raises += 1

                    if action["type"] == "check":
                        total_check_opportunities += 1

                    previous_action = action

        aggression_factor = (
            (total_bets + total_raises) / total_calls
            if total_calls > 0 else float("inf") if (total_bets + total_raises) > 0 else 0.0
        )
        check_raise_frequency = (
            total_check_raises / total_check_opportunities
            if total_check_opportunities > 0 else 0.0
        )

        return {
            "aggression_factor": aggression_factor,
            "check_raise_frequency": check_raise_frequency,
        }