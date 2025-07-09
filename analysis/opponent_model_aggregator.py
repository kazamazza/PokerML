from models.poker_session import PokerSession
from typing import Dict


class OpponentModelAggregator:
    def __init__(self):
        pass

    def aggregate(self, session: PokerSession) -> Dict[str, float]:
        """
        Aggregate a summarized profile of the villain pool in this hand.
        Produces averaged tendencies and behavior markers across all villains.
        """
        villains = session.villainProfiles.values()
        if not villains:
            return {}

        def avg(key: str) -> float:
            vals = [v.get(key) for v in villains if v.get(key) is not None]
            return sum(vals) / len(vals) if vals else 0.0

        summary = {
            "avg_aggression": avg("aggressionFactor"),
            "avg_vpip": avg("vpip"),
            "avg_pfr": avg("pfr"),
            "avg_bluff_freq": avg("bluffFrequency"),
            "avg_check_raise": avg("checkRaiseFrequency"),
            "avg_donk_bet": avg("donkBetFrequency"),
            "avg_cold_call": avg("coldCallFrequency"),
            "avg_showdown_winrate": avg("showdownWinRate"),
        }

        return summary