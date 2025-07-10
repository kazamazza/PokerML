from typing import Dict
from models.villain_action_history import VillainActionHistory


class PreflopStatsAnalyzer:
    """
    Computes preflop behavior stats: VPIP, PFR, 3-bet frequency, cold call frequency.
    """

    def analyze(self, history: VillainActionHistory) -> Dict[str, float]:
        total_hands = history.total_hands_played or 1  # avoid div-by-zero

        vpip_count = 0
        pfr_count = 0
        three_bet_count = 0
        cold_call_count = 0
        opportunity_count = 0  # hands with preflop opportunities

        for hand in history.hands:
            preflop_actions = hand.get("preflop", [])
            saw_preflop = bool(preflop_actions)
            opened = False
            three_bet = False

            for idx, action in enumerate(preflop_actions):
                act_type = action.get("type")

                if act_type in ("call", "raise"):
                    vpip_count += 1

                if act_type == "raise":
                    if not opened:
                        pfr_count += 1
                        opened = True
                    else:
                        three_bet = True

                if act_type == "call":
                    # Cold call = call when there's already been a raise before
                    any_prior_raise = any(a.get("type") == "raise" for a in preflop_actions[:idx])
                    if any_prior_raise:
                        cold_call_count += 1

            if saw_preflop:
                opportunity_count += 1
                if three_bet:
                    three_bet_count += 1

        return {
            "vpip": vpip_count / total_hands,
            "pfr": pfr_count / total_hands,
            "three_bet_rate": three_bet_count / opportunity_count if opportunity_count else 0.0,
            "villain_cold_call_frequency": cold_call_count / opportunity_count if opportunity_count else 0.0,
        }