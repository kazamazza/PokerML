from typing import Dict, Any, Optional
from analysis.hero_state_analyzer import HeroStateAnalyzer
from analysis.villain.villain_profile_aggregator import VillainProfileAggregator
from board_clusterer import BoardClusterer
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
        self.villain_profile_aggregator = VillainProfileAggregator()
        self.board_clusterer = BoardClusterer()

    def analyze(
        self,
        session: PokerSession,
        focus_seat: str
    ) -> Dict[str, Any]:
        """
        Extracts hero psychological context and aggregates villain-level psychological metrics
        for the given focus_seat.
        """
        result: Dict[str, Any] = {}

        # Hero-specific metrics (pass focus_seat if needed)
        result.update(self.hero_state_analyzer.analyze(session))

        # Board cluster key
        result["board_cluster_key"] = self.board_clusterer.get_cluster_id(session.board)

        # Identify active villains (same logic, but we care about focus_seat)
        hero = session.hero_position
        active_villains = [
            s.seat_id for s in session.seats
            if s.seat_id != hero and s.seat_id not in session.folded_players
        ]

        # Aggregators
        villain_aggregate = {
            "villain_snap_action_freq": [],
            "villain_line_pattern": [],
            "multiway_aggression_score": [],
            "villain_collusion_risk_level": [],
            "villain_overall_winrate": []
        }

        for seat in active_villains:
            history = VillainActionHistory(
                seat=seat,
                total_hands_played=1,
                hands=[HandActionHistory(hand_id=session.current_hand_id,
                                         actions=[a for a in session.action_history if a.player == seat])]
            )

            self._safe_append(
                villain_aggregate["villain_snap_action_freq"],
                self.villain_timing_analyzer.analyze(history),
                "villain_snap_action_freq"
            )
            self._safe_append(
                villain_aggregate["villain_line_pattern"],
                self.line_pattern_analyzer.analyze(history),
                "villain_line_pattern"
            )
            self._safe_append(
                villain_aggregate["multiway_aggression_score"],
                self.multiway_aggression_analyzer.analyze(history),
                "multiway_aggression_score"
            )
            self._safe_append(
                villain_aggregate["villain_collusion_risk_level"],
                self.collusion_risk_analyzer.analyze(history),
                "villain_collusion_risk_level"
            )
            self._safe_append(
                villain_aggregate["villain_overall_winrate"],
                {"villain_overall_winrate": self.villain_profile_aggregator.calculate_overall_winrate(history)},
                "villain_overall_winrate"
            )

        # Final aggregation
        result["villain_snap_action_freq"] = self._average_or_none(villain_aggregate["villain_snap_action_freq"])
        result["multiway_aggression_score"] = self._average_or_none(villain_aggregate["multiway_aggression_score"])
        result["villain_line_pattern"] = self._first_or_none(villain_aggregate["villain_line_pattern"])
        result["villain_collusion_risk_level"] = self._first_or_none(villain_aggregate["villain_collusion_risk_level"])
        result["villain_overall_winrate"] = self._average_or_none(villain_aggregate["villain_overall_winrate"])

        return result

    def _safe_append(self, target_list: list, source: Optional[Dict], key: str):
        """Appends a value from source dict to the target list if it exists and is not None."""
        if source and key in source and source[key] is not None:
            target_list.append(source[key])

    def _average_or_none(self, values: list) -> Optional[float]:
        """Returns average of values or None if empty."""
        nums = [v for v in values if isinstance(v, (int, float))]
        return sum(nums) / len(nums) if nums else None

    def _first_or_none(self, values: list) -> Optional[Any]:
        """Returns the first non-None value or None."""
        return next((v for v in values if v is not None), None)