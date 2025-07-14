from typing import Dict, Literal, cast
from analysis.psychological_analyzer import PsychologicalAnalyzer
from analysis.villain.villain_history_analyzer import VillainHistoryAnalyzer
from models.poker_ml_input import VillainProfile
from models.poker_session import PokerSession
from models.villain_action_history import HandActionHistory, VillainActionHistory

class VillainProfileBuilder:
    def __init__(
        self,
        villain_history_analyzer: VillainHistoryAnalyzer,
        psychological_analyzer: PsychologicalAnalyzer,
    ):
        self.villain_history_analyzer = villain_history_analyzer
        self.psych_analyzer = psychological_analyzer

    def build(self, session: PokerSession) -> Dict[str, VillainProfile]:
        hero = session.hero_position
        active_villains = [
            s.seat_id for s in session.seats
            if s.seat_id != hero and s.seat_id not in session.folded_players
        ]

        # Define the allowed profile_type literals:
        ALLOWED_TYPES: tuple[
            Literal["tight"],
            Literal["loose"],
            Literal["aggressive"],
            Literal["passive"],
            Literal["unknown"],
        ] = ("tight", "loose", "aggressive", "passive", "unknown")

        # Seat IDs are strings, so Dict[str, ...]
        profiles: Dict[str, VillainProfile] = {}

        for seat in active_villains:
            # 1) History stats
            actions = [a for a in session.action_history if a.player == seat]
            hand_history = HandActionHistory(hand_id=session.current_hand_id, actions=actions)
            history = VillainActionHistory(
                seat=seat,
                total_hands_played=1,
                hands=[hand_history],
            )
            stats = self.villain_history_analyzer.analyze(history)

            # 2) Psych analysis — pass focus_seat instead of mutating
            psych = self.psych_analyzer.analyze(session, focus_seat=seat)

            # 3) Narrow profile_type to the Literal union
            raw = stats.get("villain_profile_type")
            if isinstance(raw, str) and raw in ALLOWED_TYPES:
                chosen = raw
            else:
                chosen = "unknown"

            profile_type = cast(
                Literal["tight", "loose", "aggressive", "passive", "unknown"],
                chosen
            )

            profiles[seat] = VillainProfile(
                seat_id=seat,
                profile_type=profile_type,
                vpip=stats.get("villain_vpip"),
                pfr=stats.get("villain_pfr"),
                aggression_factor=stats.get("villain_aggression_factor"),
                bluff_frequency=stats.get("villain_bluff_frequency"),
                check_raise_frequency=stats.get("villain_check_raise_freq"),
                showdown_winrate=stats.get("villain_showdown_winrate"),
                cold_call_frequency=stats.get("villain_cold_call_frequency"),
                hero_bully_history=stats.get("villain_hero_bully_history"),
                hero_vs_villain_winrate=psych.get("hero_vs_villain_winrate"),
                snap_action_frequency=psych.get("villain_snap_action_freq"),
                emotional_tilt_level=psych.get("villain_emotional_tilt_level"),
                collusion_risk=psych.get("villain_collusion_risk_level"),
                overall_winrate=psych.get("villain_overall_winrate"),
                line_pattern=psych.get("villain_line_pattern"),
            )

        return profiles