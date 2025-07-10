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

        # Hero-specific metrics
        result.update(self.hero_state_analyzer.analyze(session))

        # Gather active villains
        hero = session.hero_position
        active_villains = [
            s.seat_id for s in session.seats
            if s.seat_id != hero and s.seat_id not in session.folded_players
        ]

        # Aggregate villain-based metrics
        villain_aggregate = {
            "villain_snap_action_freq": [],
            "villain_line_pattern": [],
            "multiway_aggression_score": [],
            "villain_collusion_risk_level": [],
        }

        for seat in active_villains:
            villain_actions = [a for a in session.action_history if a.player == seat]
            history = VillainActionHistory(
                seat=seat,
                total_hands_played=1,
                hands=[HandActionHistory(hand_id=session.current_hand_id, actions=villain_actions)]
            )

            villain_aggregate["villain_snap_action_freq"].append(
                self.villain_timing_analyzer.analyze(history)["villain_snap_action_freq"]
            )
            villain_aggregate["villain_line_pattern"].append(
                self.line_pattern_analyzer.analyze(history)["villain_line_pattern"]
            )
            villain_aggregate["multiway_aggression_score"].append(
                self.multiway_aggression_analyzer.analyze(history)["multiway_aggression_score"]
            )
            villain_aggregate["villain_collusion_risk_level"].append(
                self.collusion_risk_analyzer.analyze(history)["villain_collusion_risk_level"]
            )

        # Aggregate logic
        def average_or_none(vals):
            vals = [v for v in vals if v is not None]
            return sum(vals) / len(vals) if vals else None

        result["villain_snap_action_freq"] = average_or_none(villain_aggregate["villain_snap_action_freq"])
        result["multiway_aggression_score"] = average_or_none(villain_aggregate["multiway_aggression_score"])
        result["villain_line_pattern"] = villain_aggregate["villain_line_pattern"][0] if villain_aggregate["villain_line_pattern"] else None
        result["villain_collusion_risk_level"] = villain_aggregate["villain_collusion_risk_level"][0] if villain_aggregate["villain_collusion_risk_level"] else None

        return result