from typing import Dict

from models.villain_action_history import VillainActionHistory


class AggressionStatsAnalyzer:
    def analyze(self, history: VillainActionHistory) -> Dict[str, float]:
        total_bets = 0
        total_raises = 0
        total_calls = 0
        total_check_raises = 0
        total_check_opportunities = 0
        hero_targeted_aggression = 0
        total_aggressive_actions = 0

        for hand in history.hands:
            for street in ["flop", "turn", "river"]:
                actions = hand.get(street, [])
                previous_action = None

                for action in actions:
                    if action["player"] != "villain":
                        continue

                    act_type = action["type"]

                    if act_type in ("bet", "raise"):
                        total_aggressive_actions += 1
                        if action.get("target") == "hero":
                            hero_targeted_aggression += 1

                    if act_type == "bet":
                        total_bets += 1
                    elif act_type == "raise":
                        total_raises += 1
                        if previous_action and previous_action["type"] == "check":
                            total_check_raises += 1
                    elif act_type == "call":
                        total_calls += 1
                    elif act_type == "check":
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
        villain_hero_bully_history = (
            hero_targeted_aggression / total_aggressive_actions
            if total_aggressive_actions > 0 else 0.0
        )

        return {
            "villain_aggression_factor": aggression_factor,
            "villain_check_raise_freq": check_raise_frequency,
            "villain_hero_bully_history": villain_hero_bully_history,
        }