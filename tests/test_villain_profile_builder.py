from types import SimpleNamespace
from typing import Dict, Any

import pytest

from analysis.psychological_analyzer import PsychologicalAnalyzer
from analysis.villain.villain_history_analyzer import VillainHistoryAnalyzer
from models.poker_ml_input import VillainProfile
from models.poker_session import PokerSession, ActionEvent, PlayerRole, Stakes, PlayerSeat
from models.villain_action_history import VillainActionHistory
from services.villain_profile_builder import VillainProfileBuilder


@pytest.fixture
def stub_history_analyzer():
    class Stub(VillainHistoryAnalyzer):
        def analyze(self, history: VillainActionHistory) -> Dict[str, Any]:
            # return a full stats dict
            return {
                "villain_profile_type": "loose",
                "villain_vpip": 0.25,
                "villain_pfr": 0.10,
                "villain_aggression_factor": 1.5,
                "villain_bluff_frequency": 0.05,
                "villain_check_raise_freq": 0.02,
                "villain_showdown_winrate": 0.4,
                "villain_cold_call_frequency": 0.08,
                "villain_hero_bully_history": 0.12,
            }
    return Stub()

@pytest.fixture
def stub_psych_analyzer():
    class Stub(PsychologicalAnalyzer):
        def analyze(self, session: PokerSession, focus_seat: str) -> Dict[str, Any]:
            # return a full psych dict
            return {
                "hero_vs_villain_winrate": 0.55,
                "villain_snap_action_freq": 0.22,
                "villain_line_pattern": "zigzag",
                "villain_emotional_tilt_level": "calm",
                "villain_collusion_risk_level": "low",
                "villain_overall_winrate": 0.33,
            }
    return Stub()

@pytest.fixture
def builder(stub_history_analyzer, stub_psych_analyzer):
    return VillainProfileBuilder(
        villain_history_analyzer=stub_history_analyzer,
        psychological_analyzer=stub_psych_analyzer
    )

def make_session_with_one_villain() -> PokerSession:
    # 1) Stakes must be a Stakes instance, not a dict
    stakes = Stakes(big_blind=2.0, small_blind=1.0)

    # 2) Seats must be PlayerSeat models, not SimpleNamespace
    seats = [
        PlayerSeat(seat_id="BTN", player_id="hero", stack_size=100.0),
        PlayerSeat(seat_id="BB",  player_id="villain", stack_size=100.0),
    ]

    # 3) action_history must be ActionEvent instances
    action_history = [
        ActionEvent(
            player="BB",
            action="raise",
            amount=2.0,
            street="preflop",
            timestamp=1
        )
    ]

    # 4) Use the PlayerRole enum, not a raw string
    return PokerSession(
        session_id="s1",
        current_hand_id="h1",
        hero_id="hero",
        stakes=stakes,
        hero_hand=["Ah", "Kd"],
        board=["As", "9d", "2c"],
        street="flop",             # this maps to Street literal
        pot_size=6.0,
        player_count=2,
        stack_sizes={"BTN": 100.0, "BB": 100.0},
        hero_position="BTN",       # this maps to TableSeat literal
        folded_players=[],
        seats=seats,
        action_history=action_history,
        past_hand_results=[],      # list of HandResult, empty is fine
        player_role=PlayerRole.BTN_vs_BB,
    )

def test_build_creates_profile_for_active_villain(builder):
    session = make_session_with_one_villain()
    profiles = builder.build(session)
    # Should have exactly one entry, for "BB"
    assert list(profiles.keys()) == ["BB"]
    p: VillainProfile = profiles["BB"]

    # Check history‐derived stats
    assert p.profile_type == "loose"
    assert p.vpip == pytest.approx(0.25)
    assert p.pfr == pytest.approx(0.10)
    assert p.aggression_factor == pytest.approx(1.5)
    assert p.bluff_frequency == pytest.approx(0.05)
    assert p.check_raise_frequency == pytest.approx(0.02)
    assert p.showdown_winrate == pytest.approx(0.4)
    assert p.cold_call_frequency == pytest.approx(0.08)
    assert p.hero_bully_history == pytest.approx(0.12)

    # Check psych‐derived fields
    assert p.hero_vs_villain_winrate == pytest.approx(0.55)
    assert p.snap_action_frequency == pytest.approx(0.22)
    assert p.line_pattern == "zigzag"
    assert p.emotional_tilt_level == "calm"
    assert p.collusion_risk == "low"
    assert p.overall_winrate == pytest.approx(0.33)

def test_build_filters_profile_type(builder):
    # If history analyzer returns unexpected type, it falls back to "unknown"
    class BadTypeAnalyzer(type(builder.villain_history_analyzer)):
        def analyze(self, history):
            d = super().analyze(history)
            d["villain_profile_type"] = "nonsense"
            return d

    builder.villain_history_analyzer = BadTypeAnalyzer()
    session = make_session_with_one_villain()
    profiles = builder.build(session)
    assert profiles["BB"].profile_type == "unknown"