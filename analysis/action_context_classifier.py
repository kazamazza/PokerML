from models.poker_session import PokerSession
from typing import Optional, Literal

class ActionContextClassifier:
    def __init__(self):
        pass

    def classify(self, session: PokerSession) -> dict:
        """
        Classifies the current action context — aggression level, line type, etc.
        """
        action_history = session.actionHistory
        street = session.street
        preflop_action = session.calculations.preflopAction
        postflop_action = session.calculations.postflopAction
        last_aggressor = session.calculations.lastAggressor

        aggression_level = self._detect_aggression_level(action_history)
        line_type = self._classify_line(preflop_action, postflop_action)

        return {
            "aggression_level": aggression_level,
            "line_type": line_type,
            "last_aggressor": last_aggressor,
            "street": street
        }

    def _detect_aggression_level(self, history: list) -> Literal["passive", "mixed", "aggressive"]:
        raise_actions = sum(1 for act in history if act.action in ["raise", "bet"])
        call_actions = sum(1 for act in history if act.action in ["call", "check"])
        total = raise_actions + call_actions
        if total == 0:
            return "passive"
        ratio = raise_actions / total
        if ratio > 0.6:
            return "aggressive"
        elif ratio < 0.3:
            return "passive"
        return "mixed"

    def _classify_line(self, preflop: str, postflop: str) -> str:
        if "3bet" in preflop.lower():
            return "3bet pot"
        if "limp" in preflop.lower():
            return "limp pot"
        if "check" in postflop.lower():
            return "delayed line"
        return "standard"