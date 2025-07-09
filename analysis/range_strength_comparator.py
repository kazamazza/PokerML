from models.poker_session import PokerSession
from typing import Optional

class RangeStrengthComparator:
    def __init__(self):
        pass

    def compare(self, session: PokerSession) -> dict:
        """
        Compares hero's range against villains' to compute advantage metrics.
        """
        hero_range = session.calculations.rangeSummary.heroRange
        villain_ranges = session.calculations.rangeSummary.villainRanges
        range_advantage = session.calculations.rangeSummary.rangeAdvantage
        coverage = session.calculations.rangeSummary.coverage

        # Placeholder logic for deeper analysis
        hero_coverage = len(hero_range)
        villain_coverage = sum(len(v) for v in villain_ranges.values())

        relative_coverage = self._coverage_level(hero_coverage, villain_coverage)

        return {
            "range_advantage": range_advantage,
            "coverage": coverage,
            "relative_coverage": relative_coverage,
            "hero_range_size": hero_coverage,
            "villain_range_size": villain_coverage
        }

    def _coverage_level(self, hero_size: int, villain_size: int) -> str:
        ratio = hero_size / villain_size if villain_size else 1
        if ratio > 1.2:
            return "high"
        elif ratio < 0.8:
            return "low"
        return "balanced"