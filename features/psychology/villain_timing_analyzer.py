from typing import Dict
from models.constants import SNAP_ACTION_THRESHOLD_MS
from models.villain_action_history import VillainActionHistory


class VillainTimingAnalyzer:
    def __init__(self, snap_threshold_ms: int = SNAP_ACTION_THRESHOLD_MS):
        self.snap_threshold_ms = snap_threshold_ms  # e.g., 1000 ms

    def analyze(self, history: VillainActionHistory) -> Dict[str, float]:
        total_actions = 0
        snap_actions = 0

        for hand in history.hands:
            sorted_actions = sorted(
                hand.actions,
                key=lambda a: a.timestamp if a.timestamp is not None else float('inf')
            )

            for i in range(1, len(sorted_actions)):
                prev = sorted_actions[i - 1]
                curr = sorted_actions[i]

                if curr.player == history.seat and curr.timestamp and prev.timestamp:
                    delta = curr.timestamp - prev.timestamp
                    if delta <= self.snap_threshold_ms:
                        snap_actions += 1
                    total_actions += 1

        snap_freq = snap_actions / total_actions if total_actions else 0.0
        return {
            "villain_snap_action_freq": round(snap_freq, 3)
        }