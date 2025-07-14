from models.villain_action_history import VillainActionHistory

class VillainProfileAggregator:
    def calculate_overall_winrate(self, history: VillainActionHistory) -> float:
        total_bb_won = 0.0
        total_hands = len(history.hands)

        for hand in history.hands:
            # ✅ Use getattr and default to 0.0 if missing or None
            net_bb = getattr(hand, "net_bb", 0.0) or 0.0
            total_bb_won += net_bb

        if total_hands == 0:
            return 0.0

        # bb per hand → bb/100
        return (total_bb_won / total_hands) * 100