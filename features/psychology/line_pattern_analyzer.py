from typing import Dict
from models.villain_action_history import VillainActionHistory


class LinePatternAnalyzer:
    def __init__(self):
        pass

    def analyze(self, history: VillainActionHistory) -> Dict[str, str]:
        """
        Detect common line patterns like:
        - 'bet-bet-jam'
        - 'check-raise-fold'
        - 'call-call-call'
        Returns the most frequent line as a summary.
        """
        line_counter = {}

        for hand in history.hands:
            actions = [a for a in hand.actions if a.player == history.seat]
            if not actions:
                continue

            pattern = "-".join([a.action for a in actions])
            line_counter[pattern] = line_counter.get(pattern, 0) + 1

        if not line_counter:
            return {"villain_line_pattern": "unknown"}

        most_common_pattern = max(line_counter.items(), key=lambda x: x[1])[0]
        return {"villain_line_pattern": most_common_pattern}