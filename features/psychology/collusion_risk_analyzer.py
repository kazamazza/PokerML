from collections import defaultdict, Counter
from typing import Optional

from models.villain_action_history import VillainActionHistory


class CollusionRiskAnalyzer:
    def analyze(self, history: VillainActionHistory) -> Optional[str]:
        """
        Estimate the collusion risk level based on suspiciously coordinated actions
        across multiple hands between the same group of players.

        Returns:
            "low", "medium", or "high" risk
        """
        # Group actions by hand_id and by street
        hand_patterns = defaultdict(lambda: defaultdict(list))  # hand_id -> street -> list of actions

        for hand in history.hands:
            for action in hand.actions:
                hand_patterns[hand.hand_id][action.street].append((action.player, action.action))

        # Analyze patterns of coordinated folding or raising
        coordinated_raises = 0
        coordinated_folds = 0
        total_hands = len(hand_patterns)

        for hand_id, street_actions in hand_patterns.items():
            for street, actions in street_actions.items():
                if len(actions) <= 1:
                    continue

                action_counter = Counter([a[1] for a in actions])
                if action_counter.get("raise", 0) >= 2:
                    coordinated_raises += 1
                if action_counter.get("fold", 0) >= 2:
                    coordinated_folds += 1

        suspicious_activity = coordinated_raises + coordinated_folds

        if total_hands == 0:
            return "low"

        ratio = suspicious_activity / total_hands

        if ratio > 0.5:
            return "high"
        elif ratio > 0.2:
            return "medium"
        else:
            return "low"