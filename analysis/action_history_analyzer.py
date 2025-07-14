from typing import Dict, Optional
from models.poker_session import PokerSession


class ActionHistoryAnalyzer:
    def analyze(self, session: PokerSession) -> Dict[str, Optional[str]]:
        hero_actions = [a for a in session.action_history if a.player == session.hero_position]
        villain_actions = [a for a in session.action_history if a.player != session.hero_position]

        # 🧠 Heuristic: Tilted hero if they shove or overbet after a big loss
        hero_tilt_state = "neutral"
        if any(a.action in {"shove", "overbet"} for a in hero_actions):
            hero_tilt_state = "tilted"
        elif any(a.action in {"check", "fold"} for a in hero_actions[-2:]):
            hero_tilt_state = "careful"

        # 🧠 Heuristic: Session heat based on frequency of villain aggression
        villain_bets = [a for a in villain_actions if a.action in {"bet", "raise", "3bet"}]
        heat_ratio = len(villain_bets) / max(len(villain_actions), 1)

        if heat_ratio > 0.5:
            session_heat = "hot"
        elif heat_ratio < 0.2:
            session_heat = "cold"
        else:
            session_heat = "neutral"

        return {
            "hero_tilt_state": hero_tilt_state,
            "session_heat": session_heat
        }