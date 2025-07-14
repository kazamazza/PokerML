from enum import Enum


class HandCategory(str, Enum):
    HIGH_CARD    = "High Card"
    ONE_PAIR     = "One Pair"
    TWO_PAIR     = "Two Pair"
    TRIPS        = "Trips"
    SET          = "Set"
    STRAIGHT     = "Straight"
    FLUSH        = "Flush"
    FULL_HOUSE   = "Full House"
    QUADS        = "Quads"
    COMBO_DRAW   = "Combo Draw"
    UNKNOWN = "Unknown"

class HandStrength:
    def __init__(self, label: HandCategory):
        if not isinstance(label, HandCategory):
            raise ValueError(f"Invalid hand label: {label!r}; must be one of {list(HandCategory)}")
        self.label: HandCategory = label

    def __repr__(self):
        return f"HandStrength(label={self.label.value})"