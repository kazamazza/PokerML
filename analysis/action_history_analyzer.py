# ml/analysis/action_history_analyzer.py

from typing import List
from models.poker_session import ActionEvent

class ActionHistoryAnalyzer:
    def __init__(self):
        pass

    def analyze(self, actions: List[ActionEvent]) -> dict:
        """
        Analyze the sequence of actions to extract tempo, aggression shifts,
        betting patterns, and timing tells.
        """
        return {
            "recent_aggression": "medium",  # low, medium, high
            "has_recent_3bet": False,
            "has_recent_check_raise": False,
            "average_aggression_per_street": {
                "preflop": 0.3,
                "flop": 0.5,
                "turn": 0.4,
                "river": 0.2
            },
            "num_actions_this_hand": len(actions)
        }