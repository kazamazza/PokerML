from types import SimpleNamespace

import pytest

from analysis.action_history_analyzer import ActionHistoryAnalyzer
from models.poker_session import ActionEvent


@pytest.fixture
def analyzer():
    return ActionHistoryAnalyzer()


def make_session(hero_position, actions):
    """
    Build a minimal session with .hero_position and .action_history
    """
    return SimpleNamespace(hero_position=hero_position, action_history=actions)


@pytest.mark.parametrize(
    "hero_actions, expected_tilt",
    [
        # Any shove → tilted
        (["shove"], "tilted"),
        # Any overbet → tilted
        (["bet", "overbet"], "tilted"),
        # Last two include a check → careful
        (["call", "check"], "careful"),
        # Last two include a fold → careful
        (["bet", "fold"], "careful"),
        # Neither special → neutral
        (["bet", "call"], "neutral"),
    ]
)
def test_hero_tilt_state(analyzer, hero_actions, expected_tilt):
    # build hero action events
    actions = [
        ActionEvent(player="BTN", action=act, street="flop") for act in hero_actions
    ]
    # add some dummy villain actions so villain_actions list is non-empty
    actions += [
        ActionEvent(player="BB", action="call", street="flop")
    ]
    session = make_session(hero_position="BTN", actions=actions)
    result = analyzer.analyze(session)
    assert result["hero_tilt_state"] == expected_tilt


@pytest.mark.parametrize(
    "villain_actions, expected_heat",
    [
        # More than 50% of villain actions are aggressive → hot
        (["bet", "raise", "call"], "hot"),
        # Less than 20% aggressive → cold
        (["call", "fold", "check", "call", "call"], "cold"),
        # Between 20% and 50% → neutral
        (["bet", "call", "check", "call"], "neutral"),
    ]
)
def test_session_heat(analyzer, villain_actions, expected_heat):
    # build villain actions
    actions = [
        ActionEvent(player="BB", action=act, street="turn") for act in villain_actions
    ]
    # add some hero actions so hero_actions list is non-empty
    actions += [
        ActionEvent(player="BTN", action="call", street="turn")
    ]
    session = make_session(hero_position="BTN", actions=actions)
    result = analyzer.analyze(session)
    assert result["session_heat"] == expected_heat


def test_combined_behavior(analyzer):
    """
    Mixed actions to verify both fields calculated correctly together.
    """
    actions = [
        # hero does a check-then-shove
        ActionEvent(player="BTN", action="check", street="turn"),
        ActionEvent(player="BTN", action="shove", street="turn"),
        # villains mixed
        ActionEvent(player="BB", action="raise", street="turn"),
        ActionEvent(player="BB", action="call", street="turn"),
    ]
    session = make_session(hero_position="BTN", actions=actions)
    result = analyzer.analyze(session)
    # hero shoved → tilted
    assert result["hero_tilt_state"] == "tilted"
    # villain actions: 1 aggressive out of 2 → 0.5 → neutral
    assert result["session_heat"] == "neutral"