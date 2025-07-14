from types import SimpleNamespace

import pytest

from analysis.psychological_analyzer import PsychologicalAnalyzer
from models.poker_session import ActionEvent


@pytest.fixture
def analyzer():
    pa = PsychologicalAnalyzer()
    pa.hero_state_analyzer = SimpleNamespace(analyze=lambda session, focus_seat: {
        "hero_vs_villain_winrate": 0.42,
        "hero_recent_big_loss_flag": True,
        "hero_tilt_state": "tilted"
    })
    # stub each sub-analyzer
    pa.hero_state_analyzer = SimpleNamespace(analyze=lambda session: {
        "hero_vs_villain_winrate": 0.42,
        "hero_recent_big_loss_flag": True,
        "hero_tilt_state": "tilted"
    })
    pa.board_clusterer = SimpleNamespace(get_cluster_id=lambda board: 7)
    pa.villain_timing_analyzer = SimpleNamespace(analyze=lambda history: {"villain_snap_action_freq": 0.11})
    pa.line_pattern_analyzer = SimpleNamespace(analyze=lambda history: {"villain_line_pattern": "zigzag"})
    pa.multiway_aggression_analyzer = SimpleNamespace(analyze=lambda history: {"multiway_aggression_score": 0.22})
    pa.collusion_risk_analyzer = SimpleNamespace(analyze=lambda history: {"villain_collusion_risk_level": "medium"})
    pa.villain_profile_aggregator = SimpleNamespace(calculate_overall_winrate=lambda history: 0.33)
    return pa


def make_session():
    seats = [SimpleNamespace(seat_id="BTN"), SimpleNamespace(seat_id="BB")]
    # one villain action for BB: use real ActionEvent
    action_history = [ActionEvent(player="BB", action="bet", street="flop")]
    return SimpleNamespace(
        hero_position="BTN",
        seats=seats,
        folded_players=[],
        action_history=action_history,
        current_hand_id="h1",
        board=["As", "Kd", "2c"],
        past_hand_results=[],
    )


def test_analyze_aggregates_all_metrics(analyzer):
    session = make_session()
    result = analyzer.analyze(session, focus_seat="BB")

    # Hero-specific metrics
    assert result["hero_vs_villain_winrate"] == pytest.approx(0.42)
    assert result["hero_recent_big_loss_flag"] is True
    assert result["hero_tilt_state"] == "tilted"

    # Board cluster
    assert result["board_cluster_key"] == 7

    # Villain-level aggregated metrics (only one villain => same as stub)
    assert result["villain_snap_action_freq"] == pytest.approx(0.11)
    assert result["multiway_aggression_score"] == pytest.approx(0.22)
    assert result["villain_line_pattern"] == "zigzag"
    assert result["villain_collusion_risk_level"] == "medium"
    assert result["villain_overall_winrate"] == pytest.approx(0.33)

    # Keys should match exactly this set
    expected_keys = {
        "hero_vs_villain_winrate",
        "hero_recent_big_loss_flag",
        "hero_tilt_state",
        "board_cluster_key",
        "villain_snap_action_freq",
        "multiway_aggression_score",
        "villain_line_pattern",
        "villain_collusion_risk_level",
        "villain_overall_winrate",
    }
    assert set(result.keys()) == expected_keys
