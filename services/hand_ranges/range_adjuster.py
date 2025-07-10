from typing import Dict, List


class RangeAdjuster:
    weights: Dict[str, float] = {
        "tight": 0.8,
        "loose": 1.2,
        "aggressive": 1.1,
        "passive": 0.9,
        "maniac": 1.5,
        "calling-station": 0.7,
        "default": 1.0,
    }

    @classmethod
    def apply(cls, base_range: List[str], villain_type: str) -> List[Dict[str, float]]:
        factor = cls.weights.get(villain_type, 1.0)
        return [
            {"hand": hand, "weight": max(min(1.0 * factor, 2.0), 0.1)}
            for hand in base_range
        ]