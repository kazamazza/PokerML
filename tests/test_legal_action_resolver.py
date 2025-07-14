import pytest

from helper.legal_action_resolver import LegalActionResolver
from models.poker_ml_input import BetAction


@pytest.fixture
def resolver():
    return LegalActionResolver()


def test_all_in_returns_only_check(resolver):
    actions = [
        BetAction(player="BTN", action="bet", size=5.0),
        BetAction(player="BB", action="raise", size=10.0),
    ]
    legal = resolver.resolve(
        street="flop",
        stack=20.0,
        pot_size=15.0,
        bet_history=actions,
        is_all_in=True
    )
    assert legal == ["check"]


def test_preflop_with_no_raise_includes_limp(resolver):
    bet_history = [
        BetAction(player="SB", action="call", size=1.0),
        BetAction(player="BB", action="call", size=2.0),
    ]
    legal = resolver.resolve(
        street="preflop",
        stack=100.0,
        pot_size=10.0,
        bet_history=bet_history,
        is_all_in=False
    )
    # should include fold, call, limp, and raise sizes [5,10]
    expected = sorted(["fold", "call", "limp", "raise", "raise_5", "raise_10"])
    assert legal == expected


def test_preflop_with_existing_raise_excludes_limp(resolver):
    bet_history = [
        BetAction(player="SB", action="raise", size=5.0),
    ]
    legal = resolver.resolve(
        street="preflop",
        stack=50.0,
        pot_size=10.0,
        bet_history=bet_history,
        is_all_in=False
    )
    # limp should be omitted
    expected = sorted(["fold", "call", "raise", "raise_5", "raise_10"])
    assert legal == expected


@pytest.mark.parametrize("street", ["flop", "turn", "river"])
def test_postflop_does_not_include_limp(resolver, street):
    bet_history = []
    legal = resolver.resolve(
        street=street,
        stack=30.0,
        pot_size=8.0,
        bet_history=bet_history,
        is_all_in=False
    )
    # No limp outside preflop
    # raise sizes: 0.5*8=4, 8 → both under stack
    expected = sorted(["fold", "call", "raise", "raise_4", "raise_8"])
    assert legal == expected


def test_raise_sizes_above_stack_are_filtered(resolver):
    # pot_size yields raises [20,40] but stack is only 25
    bet_history = []
    legal = resolver.resolve(
        street="river",
        stack=25.0,
        pot_size=40.0,
        bet_history=bet_history,
        is_all_in=False
    )
    # 0.5*40=20 is allowed, 40 is not
    expected = sorted(["fold", "call", "raise", "raise_20"])
    assert legal == expected