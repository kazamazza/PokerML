from typing import Dict, Any

from analysis.hero_state_analyzer import HeroStateAnalyzer
from features.psychology.multiway_aggression_analyzer import MultiwayAggressionAnalyzer
from models.poker_session import PokerSession


class SessionContextAnalyzer:
    def __init__(self):
        self.hero_state_analyzer = HeroStateAnalyzer()
        self.multiway_aggression_analyzer = MultiwayAggressionAnalyzer()

    def analyze(self, session: PokerSession) -> Dict[str, Any]:
        """
        Returns only the session‐level psychology metrics:
          - hero_vs_villain_winrate
          - hero_recent_big_loss_flag
          - hero_tilt_state
          - multiway_aggression_score
        """
        metrics: Dict[str, Any] = {}
        # Hero‐state (winrate, tilt, etc.)
        metrics.update(self.hero_state_analyzer.analyze(session))
        # Multiway aggression across all active villains
        raw = self.multiway_aggression_analyzer.analyze(session)
        if isinstance(raw, dict):
            metrics["multiway_aggression_score"] = raw.get("multiway_aggression_score")
        else:
            metrics["multiway_aggression_score"] = raw
        return metrics