from typing import Union, Dict

from models.poker_session import PokerSession
from models.villain_action_history import VillainActionHistory, HandActionHistory

AGGRESSIVE_ACTIONS = {"bet", "raise", "3bet", "shove"}

class MultiwayAggressionAnalyzer:
    def __init__(self):
        pass

    def analyze(
        self,
        source: Union[VillainActionHistory, PokerSession]
    ) -> Dict[str, float]:
        """
        If `source` is a VillainActionHistory, computes that villain’s multiway aggression.
        If `source` is a PokerSession, averages multiway aggression across all active villains.
        """
        if isinstance(source, PokerSession):
            # session‐level: average across villains
            hero = source.hero_position
            seats = [
                s.seat_id for s in source.seats
                if s.seat_id != hero and s.seat_id not in source.folded_players
            ]
            scores = []
            for seat in seats:
                # extract that villain’s actions into a single-hand history
                actions = [a for a in source.action_history if a.player == seat]
                hand_hist = HandActionHistory(
                    hand_id=source.current_hand_id,
                    actions=actions
                )
                hist = VillainActionHistory(
                    seat=seat,
                    total_hands_played=1,
                    hands=[hand_hist]
                )
                score = self._compute_score(hist)
                scores.append(score)

            avg = sum(scores) / len(scores) if scores else 0.0
            return {"multiway_aggression_score": round(avg, 3)}

        else:
            # single-villain history
            return {"multiway_aggression_score": self._compute_score(source)}

    def _compute_score(self, history: VillainActionHistory) -> float:
        total_spots = 0
        aggro_actions = 0

        for hand in history.hands:
            players = {a.player for a in hand.actions}
            if len(players) < 3:
                continue
            villain_acts = [a for a in hand.actions if a.player == history.seat]
            if not villain_acts:
                continue

            total_spots += 1
            if any(a.action in AGGRESSIVE_ACTIONS for a in villain_acts):
                aggro_actions += 1

        if total_spots == 0:
            return 0.0
        return round(aggro_actions / total_spots, 3)