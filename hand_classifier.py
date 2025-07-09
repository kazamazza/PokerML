from typing import List, Dict


class HandStrength:
    def __init__(self, label: str, score: float):
        self.label = label  # e.g., "Top Pair", "Overpair", "Flush Draw"
        self.score = score  # Normalized 0–1 strength score

    def __repr__(self):
        return f"HandStrength(label={self.label}, score={self.score})"


class HandClassifier:
    def __init__(self):
        # Placeholder — later this might use preflop class maps, suit graphs, etc.
        pass

    def classify(self, hero_hand: str, board_cards: List[str]) -> HandStrength:
        """
        Args:
            hero_hand: e.g. "AhKs"
            board_cards: e.g. ["Ad", "7c", "2h"]

        Returns:
            HandStrength: qualitative label + numeric strength score
        """
        # TODO: Replace with real logic — for now simple high card check
        hole_ranks = {card[0] for card in [hero_hand[:2], hero_hand[2:]]}
        board_ranks = {card[0] for card in board_cards}

        if hole_ranks & board_ranks:
            return HandStrength("Pair", 0.4)
        else:
            return HandStrength("High Card", 0.1)