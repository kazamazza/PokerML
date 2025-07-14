import pytest
from types import SimpleNamespace

from analysis.session_context_analyzer import SessionContextAnalyzer
from models.poker_session import PokerSession


@pytest.fixture
def analyzer():
    sca = SessionContextAnalyzer()
    # Stub the hero state analyzer
    sca.hero_state_analyzer = SimpleNamespace(analyze=lambda session: {
        "hero_vs_villain_winrate": 0.65,
        "hero_recent_big_loss_flag": False,
        "hero_tilt_state": "neutral",
    })
    # Stub the multiway aggression analyzer
    sca.multiway_aggression_analyzer = SimpleNamespace(analyze=lambda session: 0.33)
    return sca


def make_session() -> PokerSession:
    # minimal PokerSession stub: only passed into analyzers, which are stubbed
    return SimpleNamespace()


def test_analyze_combines_hero_and_multiway_metrics(analyzer):
    session = make_session()
    result = analyzer.analyze(session)

    # Should include both hero-state keys and multiway aggression
    assert result["hero_vs_villain_winrate"] == pytest.approx(0.65)
    assert result["hero_recent_big_loss_flag"] is False
    assert result["hero_tilt_state"] == "neutral"
    assert result["multiway_aggression_score"] == pytest.approx(0.33)


def test_analyze_contains_only_expected_keys(analyzer):
    session = make_session()
    result = analyzer.analyze(session)
    expected_keys = {
        "hero_vs_villain_winrate",
        "hero_recent_big_loss_flag",
        "hero_tilt_state",
        "multiway_aggression_score",
    }
    assert set(result.keys()) == expected_keys
