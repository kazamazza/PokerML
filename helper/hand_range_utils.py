from typing import List


class HandRangeUtils:
    @staticmethod
    def merge_ranges(ranges: List[List[str]]) -> List[str]:
        """Combine multiple hand range lists into a unique set of combos."""
        merged = set()
        for r in ranges:
            merged.update(r)
        return list(merged)