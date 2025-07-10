class HandStrength:
    def __init__(self, label: str, score: float):
        self.label = label  # e.g., "Top Pair", "Overpair", "Combo Draw"
        self.score = score  # Normalized float from 0.0 to 1.0

    def __repr__(self):
        return f"HandStrength(label={self.label}, score={round(self.score, 2)})"