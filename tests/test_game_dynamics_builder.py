import pytest
from types import SimpleNamespace

from analysis.action_history_analyzer import ActionHistoryAnalyzer
from models.poker_ml_input import GameDynamics, BetAction
from models.poker_session import ActionEvent
from services.game_dynamics_builder import GameDynamicsBuilder

@pytest.fixture
def analyzer():
    return ActionHistoryAnalyzer()

@pytest.fixture
def builder(analyzer):
    return GameDynamicsBuilder(action_history_analyzer=analyzer)


def make_session(actions, hero_position="BTN") -> SimpleNamespace:
    # Minimal session for dynamics
    return SimpleNamespace(
        hero_position=hero_position,
        action_history=actions
    )

# --- Tests for ActionHistoryAnalyzer directly ---

@pytest.mark.parametrize(
    "hero_moves,expected_tilt",
    [
        (["shove"], "tilted"),
        (["overbet"], "tilted"),
        (["check", "fold"], "careful"),
        ([], "neutral"),
    ]
)
def test_action_history_tilt_states(analyzer, hero_moves, expected_tilt):
    actions = []
    # hero actions
    for move in hero_moves:
        actions.append(ActionEvent(player="BTN", action=move, street="flop"))
    # add a villain action so villain_actions non-empty
    actions.append(ActionEvent(player="BB", action="bet", street="flop"))

    session = make_session(actions)
    stats = analyzer.analyze(session)
    assert stats["hero_tilt_state"] == expected_tilt

@pytest.mark.parametrize(
    "villain_moves,expected_heat",
    [
        (["bet", "raise", "3bet"], "hot"),  # 100% aggression
        (["call", "fold", "check"], "cold"),  # 0% aggression
        (["bet", "call", "fold", "call", "check"], "neutral"),  # 20% = neutral
    ]
)
def test_action_history_session_heat(analyzer, villain_moves, expected_heat):
    actions = []
    # villain actions
    for move in villain_moves:
        actions.append(ActionEvent(player="BB", action=move, street="turn"))
    # add hero action so hero_actions non-empty
    actions.append(ActionEvent(player="BTN", action="call", street="turn"))

    session = make_session(actions)
    stats = analyzer.analyze(session)
    assert stats["session_heat"] == expected_heat

# --- Tests for GameDynamicsBuilder ---

def test_game_dynamics_builder_builds_correctly(builder, monkeypatch):
    # Stub analyzer to return known stats
    monkeypatch.setattr(builder.analyzer, 'analyze', lambda session: {
        "hero_tilt_state": "tilted",
        "session_heat": "hot"
    })

    # Create action_history with various events
    actions = [
        ActionEvent(player="BTN", action="fold", street="river"),
        ActionEvent(player="BB", action="bet", amount=5.0, street="river"),
        ActionEvent(player="SB", action="raise", amount=3.0, street="river"),
        ActionEvent(player="CO", action="call", amount=2.0, street="river"),
        ActionEvent(player="BB", action="check", street="river"),  # should be filtered
    ]

    session = make_session(actions)
    gd = builder.build(session)
    assert isinstance(gd, GameDynamics)

    # bet_history: only bet, raise, call, 3bet, shove
    expected_actions = [a for a in actions if a.action in {"bet", "raise", "call", "3bet", "shove"}]
    # Compare by attributes
    assert len(gd.bet_history) == len(expected_actions)
    for ba, ev in zip(gd.bet_history, expected_actions):
        assert isinstance(ba, BetAction)
        assert ba.player == ev.player
        assert ba.action == ev.action
        assert ba.size == pytest.approx(ev.amount or 0.0)

    assert gd.hero_tilt_state == "tilted"
    assert gd.session_heat == "hot"

