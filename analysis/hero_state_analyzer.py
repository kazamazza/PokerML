from typing import Dict, Any
from models.hand_result import HandResult
from models.poker_session import PokerSession


class HeroStateAnalyzer:
    def __init__(self, big_loss_threshold_bb: float = 50.0):
        self.big_loss_threshold_bb = big_loss_threshold_bb

    def analyze(self, session: PokerSession) -> Dict[str, Any]:
        """
        Analyze the hero's psychological state based on historical outcomes.
        """
        hero_id = session.hero_id
        results: list[HandResult] = session.past_hand_results or []
        villain_ids = [s.player_id for s in session.seats if s.seat_id != session.hero_position]

        # 1. Winrate vs Villains
        vs_villain_wins = 0
        vs_villain_total = 0
        for hand in results:
            if hand.hero_id == hero_id and hand.villain_id in villain_ids:
                vs_villain_total += 1
                if hand.hero_won:
                    vs_villain_wins += 1

        winrate = vs_villain_wins / vs_villain_total if vs_villain_total else None

        # 2. Recent big loss detection (last hand)
        recent_loss_flag = False
        if results:
            last = results[-1]
            if last.hero_id == hero_id and last.net_bb < -self.big_loss_threshold_bb:
                recent_loss_flag = True

        # 3. Tilt state (basic heuristic)
        if recent_loss_flag and winrate is not None and winrate < 0.3:
            tilt_state = "tilted"
        elif winrate is not None and winrate > 0.6:
            tilt_state = "confident"
        elif recent_loss_flag:
            tilt_state = "careful"
        else:
            tilt_state = "neutral"

        return {
            "hero_vs_villain_winrate": winrate,
            "hero_recent_big_loss_flag": recent_loss_flag,
            "hero_tilt_state": tilt_state
        }