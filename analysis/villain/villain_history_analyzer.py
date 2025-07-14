from typing import Dict

from models.villain_action_history import VillainActionHistory


class VillainHistoryAnalyzer:
    def analyze(self, history: VillainActionHistory) -> Dict[str, float]:
        """
        Analyzes a villain's action history and returns aggregate stats.
        """
        actions = []
        for hand in history.hands:
            actions.extend(hand.actions)

        total_hands = len(history.hands)
        if total_hands == 0:
            return self._empty_result()

        result = {
            "villain_profile_type": "unknown",  # Set this later if desired
            "villain_vpip": self._compute_vpip(actions, total_hands),
            "villain_pfr": self._compute_pfr(actions, total_hands),
            "villain_aggression_factor": self._compute_aggression(actions),
            "villain_bluff_frequency": self._compute_bluff_freq(actions),
            "villain_check_raise_freq": self._compute_check_raise_freq(actions),
            "villain_showdown_winrate": self._compute_showdown_winrate(history),
            "villain_cold_call_frequency": self._compute_cold_call_freq(actions),
            "villain_hero_bully_history": self._compute_bully_factor(actions),
        }

        return result

    def _empty_result(self) -> Dict[str, float]:
        return {
            "villain_profile_type": "unknown",
            "villain_vpip": 0.0,
            "villain_pfr": 0.0,
            "villain_aggression_factor": 0.0,
            "villain_bluff_frequency": 0.0,
            "villain_check_raise_freq": 0.0,
            "villain_showdown_winrate": 0.0,
            "villain_cold_call_frequency": 0.0,
            "villain_hero_bully_history": 0.0,
        }

    def _compute_vpip(self, actions, total_hands):
        vpip_actions = [a for a in actions if a.street == "preflop" and a.action in {"call", "raise"}]
        return len(vpip_actions) / total_hands

    def _compute_pfr(self, actions, total_hands):
        pfr_actions = [a for a in actions if a.street == "preflop" and a.action in {"raise", "3bet", "shove"}]
        return len(pfr_actions) / total_hands

    def _compute_aggression(self, actions):
        bets = sum(1 for a in actions if a.action in {"bet", "raise"})
        calls = sum(1 for a in actions if a.action == "call")
        return round(bets / calls, 2) if calls > 0 else float(bets)

    def _compute_bluff_freq(self, actions):
        bluff_attempts = sum(1 for a in actions if a.action == "bet" and a.street in {"turn", "river"})
        total_bets = sum(1 for a in actions if a.action == "bet")
        return bluff_attempts / total_bets if total_bets > 0 else 0.0

    def _compute_check_raise_freq(self, actions):
        check_raises = sum(1 for a in actions if a.action == "raise" and "check" in a.context if hasattr(a, "context"))
        total_raises = sum(1 for a in actions if a.action == "raise")
        return check_raises / total_raises if total_raises > 0 else 0.0

    def _compute_showdown_winrate(self, history: VillainActionHistory):
        wins = sum(1 for h in history.hands if getattr(h, "won_showdown", False))
        return wins / len(history.hands) if history.hands else 0.0

    def _compute_cold_call_freq(self, actions):
        cold_calls = sum(1 for a in actions if a.street == "preflop" and a.action == "call" and not getattr(a, "had_raised_before", False))
        total_preflop = sum(1 for a in actions if a.street == "preflop")
        return cold_calls / total_preflop if total_preflop > 0 else 0.0

    def _compute_bully_factor(self, actions):
        hero_targets = [a for a in actions if a.target == "hero"] if any(hasattr(a, "target") for a in actions) else []
        aggro_hero = [a for a in hero_targets if a.action in {"bet", "raise"}]
        return len(aggro_hero) / len(hero_targets) if hero_targets else 0.0