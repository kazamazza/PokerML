from models.villain_action_history import VillainActionHistory


class VillainProfileAggregator:
    def calculate_overall_winrate(self, history: VillainActionHistory) -> float:
        """
        Computes long-term winrate in bb/100.
        Assumes each HandActionHistory contains net_bb field.
        """
        total_bb_won = 0.0
        total_hands = len(history.hands)

        for hand in history.hands:
            net = hand.get("net_bb", 0.0)  # must be populated earlier
            total_bb_won += net

        if total_hands == 0:
            return 0.0
        return (total_bb_won / total_hands) * 100  # convert to bb/100