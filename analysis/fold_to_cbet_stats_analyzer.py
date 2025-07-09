from typing import Dict

from models.villain_action_history import VillainActionHistory


class FoldToCBetStatsAnalyzer:
    def analyze(self, history: VillainActionHistory) -> Dict[str, float]:
        fold_to_cbet_flop = 0
        cbet_flop_opportunities = 0

        fold_to_cbet_turn = 0
        cbet_turn_opportunities = 0

        for hand in history.hands:
            for street in ["flop", "turn"]:
                actions = hand.get(street, [])
                cbet_detected = False
                villain_folded = False

                for i, action in enumerate(actions):
                    if action["player"] == "hero" and action["type"] in ("bet", "raise") and i == 0:
                        # Hero leads out first action = c-bet candidate
                        cbet_detected = True
                    elif cbet_detected and action["player"] == "villain":
                        if action["type"] == "fold":
                            villain_folded = True
                        break  # Only care about immediate response to c-bet

                if cbet_detected:
                    if street == "flop":
                        cbet_flop_opportunities += 1
                        if villain_folded:
                            fold_to_cbet_flop += 1
                    elif street == "turn":
                        cbet_turn_opportunities += 1
                        if villain_folded:
                            fold_to_cbet_turn += 1

        return {
            "fold_to_cbet_flop": fold_to_cbet_flop / cbet_flop_opportunities if cbet_flop_opportunities else 0.0,
            "fold_to_cbet_turn": fold_to_cbet_turn / cbet_turn_opportunities if cbet_turn_opportunities else 0.0,
        }