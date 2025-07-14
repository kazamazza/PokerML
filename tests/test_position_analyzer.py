import pytest
from types import SimpleNamespace

from analysis.position_analyzer import PositionAnalyzer
from models.poker_ml_input import PositionContext
from models.poker_session import TableSeat, ActionEvent


@pytest.fixture
def analyzer():
    return PositionAnalyzer()


def make_session(
    hero_position: TableSeat,
    stack_sizes: dict,
    folded_players: list,
    action_history: list,
    calculations=None
) -> SimpleNamespace:
    return SimpleNamespace(
        hero_position=hero_position,
        stack_sizes=stack_sizes,
        folded_players=folded_players,
        action_history=action_history,
        calculations=calculations
    )


def test_no_villains(analyzer):
    sess = make_session(
        hero_position="BTN",
        stack_sizes={"BTN": 100.0},
        folded_players=[],
        action_history=[],
        calculations=None
    )
    ctx: PositionContext = analyzer.analyze(sess)
    assert ctx.in_position is True
    assert ctx.is_heads_up is False
    assert ctx.is_multiway is False
    assert ctx.aggressor_position is None


@pytest.mark.parametrize(
    "stack, folded, expected_heads_up, expected_multiway",
    [
        ({"BTN": 100.0, "BB": 50.0}, [], True, False),   # heads-up
        ({"BTN": 100.0}, [], False, False),                # solo hero
        ({"BTN": 100.0, "BB": 50.0, "CO": 80.0}, [], False, True),  # three-way
        ({"BTN": 100.0, "BB": 50.0, "CO": 80.0}, ["CO"], True, False),  # folded to heads-up
    ]
)
def test_heads_up_and_multiway(analyzer, stack, folded, expected_heads_up, expected_multiway):
    sess = make_session(
        hero_position="BTN",
        stack_sizes=stack,
        folded_players=folded,
        action_history=[],
        calculations=None
    )
    ctx = analyzer.analyze(sess)
    assert ctx.is_heads_up is expected_heads_up
    assert ctx.is_multiway is expected_multiway


def test_uses_calculations_lastAggressor(analyzer):
    stack = {"BTN": 100.0, "BB": 50.0}
    calc = SimpleNamespace(lastAggressor="BB")
    sess = make_session(
        hero_position="BTN",
        stack_sizes=stack,
        folded_players=[],
        action_history=[],
        calculations=calc
    )
    ctx = analyzer.analyze(sess)
    assert ctx.aggressor_position == "BB"


@pytest.mark.parametrize(
    "events, expected_agg",
    [
        ([("BB", "bet"), ("BTN", "call")], "BB"),
        ([("BTN", "check"), ("BB", "raise")], "BB"),
        ([("BTN", "fold")], None),
    ]
)
def test_scans_action_history_for_aggressor(analyzer, events, expected_agg):
    stack = {"BTN": 100.0, "BB": 50.0}
    actions = [
        ActionEvent(player=player, action=action, street="flop")
        for player, action in events
    ]
    sess = make_session(
        hero_position="BTN",
        stack_sizes=stack,
        folded_players=[],
        action_history=actions,
        calculations=None
    )
    ctx = analyzer.analyze(sess)
    assert ctx.aggressor_position == expected_agg