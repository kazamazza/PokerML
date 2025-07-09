from typing import Dict
from models.villain_action_history import VillainActionHistory


class CBetStatsAnalyzer:
    def analyze(self, history: VillainActionHistory) -> Dict[str, float]:
        flop_cbets = 0
        flop_opportunities = 0

        turn_cbets = 0
        turn_opportunities = 0

        for hand in history.hands:
            flop_actions = hand.get("flop", [])
            turn_actions = hand.get("turn", [])
            preflop_aggressor = self._was_aggressor_preflop(hand)

            if preflop_aggressor and flop_actions:
                flop_opportunities += 1
                if self._did_cbet(flop_actions):
                    flop_cbets += 1

            if preflop_aggressor and turn_actions:
                turn_opportunities += 1
                if self._did_cbet(turn_actions):
                    turn_cbets += 1

        return {
            "cbet_flop": flop_cbets / flop_opportunities if flop_opportunities > 0 else 0.0,
            "cbet_turn": turn_cbets / turn_opportunities if turn_opportunities > 0 else 0.0,
        }

    def _was_aggressor_preflop(self, hand: dict) -> bool:
        preflop = hand.get("preflop", [])
        return any(action["type"] == "raise" for action in preflop)

    def _did_cbet(self, street_actions: list) -> bool:
        return street_actions and street_actions[0]["type"] == "bet"