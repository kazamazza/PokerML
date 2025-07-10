from typing import Dict, Any

from analysis.hero_state_analyzer import HeroStateAnalyzer
from features.psychology.collusion_risk_analyzer import CollusionRiskAnalyzer
from features.psychology.line_pattern_analyzer import LinePatternAnalyzer
from features.psychology.multiway_aggression_analyzer import MultiwayAggressionAnalyzer
from features.psychology.villain_timing_analyzer import VillainTimingAnalyzer
from models.poker_session import PokerSession
from models.villain_action_history import VillainActionHistory, HandActionHistory


class PsychologicalAnalyzer:
    def __init__(self):
        self.hero_state_analyzer = HeroStateAnalyzer()
        self.villain_timing_analyzer = VillainTimingAnalyzer()
        self.line_pattern_analyzer = LinePatternAnalyzer()
        self.multiway_aggression_analyzer = MultiwayAggressionAnalyzer()
        self.collusion_risk_analyzer = CollusionRiskAnalyzer()

    def analyze(self, session: PokerSession) -> Dict[str, Any]:
        result = {}

        # 1. Analyze hero state (needs full session)
        result.update(self.hero_state_analyzer.analyze(session))

        # 2. Prepare villain action history
        hero = session.hero_position
        active_villains = [
            s.seat_id for s in session.seats
            if s.seat_id != hero and s.seat_id not in session.folded_players
        ]

        for seat in active_villains:
            villain_actions = [a for a in session.action_history if a.player == seat]

            history = VillainActionHistory(
                seat=seat,
                total_hands_played=1,
                hands=[HandActionHistory(hand_id=session.current_hand_id, actions=villain_actions)]
            )

            # Feed villain-specific analyzers
            result.update(self.villain_timing_analyzer.analyze(history))
            result.update(self.line_pattern_analyzer.analyze(history))
            result.update(self.multiway_aggression_analyzer.analyze(history))
            result["villain_collusion_risk_level"] = self.collusion_risk_analyzer.analyze(history)

        return result