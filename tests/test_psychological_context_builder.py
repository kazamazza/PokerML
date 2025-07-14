import pytest
from types import SimpleNamespace

from models.poker_ml_input import PsychologicalContext
from services.psychological_context_builder import PsychologicalContextBuilder


@pytest.fixture
def session_ctx_analyzer():
    stub = SimpleNamespace()
    stub.analyze = lambda session: {
        "hero_recent_big_loss_flag": True,
        "multiway_aggression_score": 0.77,
    }
    return stub

@pytest.fixture
def board_analyzer():
    return SimpleNamespace(get_cluster_id=lambda board: 42)

@pytest.fixture
def builder(session_ctx_analyzer, board_analyzer):
    return PsychologicalContextBuilder(
        session_context_analyzer=session_ctx_analyzer,
        board_analyzer=board_analyzer
    )

@pytest.fixture
def session():
    # minimal PokerSession stub
    return SimpleNamespace(board=["As", "Kd", "2c"])


def test_build_returns_psychological_context(builder, session):
    psych = builder.build(session)
    assert isinstance(psych, PsychologicalContext)
    assert psych.hero_recent_big_loss_flag is True
    assert psych.multiway_aggression_score == pytest.approx(0.77)
    assert psych.board_cluster_key == 42


def test_build_handles_missing_metrics(builder, session):
    # Make analyzer return empty dict
    builder.session_ctx.analyze = lambda session: {}
    psych = builder.build(session)
    # Missing keys should result in None
    assert psych.hero_recent_big_loss_flag is None
    assert psych.multiway_aggression_score is None
    assert psych.board_cluster_key == 42