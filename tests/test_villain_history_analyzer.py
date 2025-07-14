import pytest

from analysis.villain.villain_history_analyzer import VillainHistoryAnalyzer
from models.poker_session import ActionEvent
from models.villain_action_history import HandActionHistory, VillainActionHistory


@pytest.fixture
def analyzer():
    return VillainHistoryAnalyzer()


@pytest.mark.parametrize(
    "actions, total_hands, expected_vpip, expected_pfr",
    [
        # No hands => _empty_result applies in analyze(), but here we test compute methods directly
        (
            [ActionEvent(player="BB", action="call", street="preflop")],
            1,
            1.0,  # vpip: 1 call preflop / 1 hand
            0.0,  # pfr: no raises
        ),
        (
            [ActionEvent(player="BB", action="raise", street="preflop"),
             ActionEvent(player="BB", action="3bet", street="preflop"),
            ],
            1,
            1.0,  # two vpip actions count per hand, but vpip= len(actions_preflop_call_raise)/total_hands = 2/1 = 2.0? Actually only count 'call' or 'raise' so vpip=1/1
            1.0,  # pfr: two actions in pfr set => 2/1 = 2.0? but normalized to float => 2.0
        ),
    ]
)
def test_compute_vpip_and_pfr(analyzer, actions, total_hands, expected_vpip, expected_pfr):
    # Build two identical hands if total_hands >1
    hands = [HandActionHistory(hand_id="h1", actions=actions)] * total_hands
    history = VillainActionHistory(seat="BB", total_hands_played=total_hands, hands=hands)

    result = analyzer.analyze(history)
    assert pytest.approx(expected_vpip) == result["villain_vpip"]
    assert pytest.approx(expected_pfr) == result["villain_pfr"]


def test_empty_history_returns_zeros(analyzer):
    history = VillainActionHistory(seat="BB", total_hands_played=0, hands=[])
    result = analyzer.analyze(history)
    for key in [
        "villain_vpip", "villain_pfr", "villain_aggression_factor",
        "villain_bluff_frequency", "villain_check_raise_freq",
        "villain_showdown_winrate", "villain_cold_call_frequency",
        "villain_hero_bully_history"
    ]:
        assert result[key] == pytest.approx(0.0)
    assert result["villain_profile_type"] == "unknown"


def test_compute_aggression_and_bluff(analyzer):
    actions = [
        ActionEvent(player="BB", action="bet", street="turn"),
        ActionEvent(player="BB", action="raise", street="river"),
        ActionEvent(player="BB", action="call", street="river"),
    ]
    hand = HandActionHistory(hand_id="h2", actions=actions)
    history = VillainActionHistory(seat="BB", total_hands_played=1, hands=[hand])

    result = analyzer.analyze(history)
    # aggression: bets=2 (bet+raise), calls=1 => 2.0
    assert result["villain_aggression_factor"] == pytest.approx(2.0)
    # bluff: only "bet" on turn/river counts => 1 bet / 1 total bet = 1.0
    assert result["villain_bluff_frequency"] == pytest.approx(1.0)


def test_compute_check_raise_freq(analyzer):
    actions = [
        ActionEvent(player="BB", action="raise", street="flop", is_check_raise=True),
        ActionEvent(player="BB", action="raise", street="flop", is_check_raise=False),
    ]
    hand = HandActionHistory(hand_id="h3", actions=actions)
    history = VillainActionHistory(seat="BB", total_hands_played=1, hands=[hand])

    result = analyzer.analyze(history)
    # 1 check_raise out of 2 total raises
    assert result["villain_check_raise_freq"] == pytest.approx(0.5)


def test_compute_showdown_winrate(analyzer):
    # Pydantic models accept extra attributes on HandActionHistory for showdowns
    h1 = HandActionHistory(hand_id="h4", actions=[])
    h2 = HandActionHistory(hand_id="h5", actions=[])
    # monkeypatch the won_showdown
    object.__setattr__(h1, "won_showdown", True)
    object.__setattr__(h2, "won_showdown", False)
    history = VillainActionHistory(seat="BB", total_hands_played=2, hands=[h1, h2])
    result = analyzer.analyze(history)
    assert result["villain_showdown_winrate"] == pytest.approx(0.5)


def test_compute_cold_call_freq(analyzer):
    actions = [
        ActionEvent(player="BB", action="call", street="preflop", amount=None, timestamp=None, target=None, had_raised_before=False),
        ActionEvent(player="BB", action="call", street="preflop", amount=None, timestamp=None, target=None, had_raised_before=True),
    ]
    hand = HandActionHistory(hand_id="h6", actions=actions)
    history = VillainActionHistory(seat="BB", total_hands_played=1, hands=[hand])
    result = analyzer.analyze(history)
    assert result["villain_cold_call_frequency"] == pytest.approx(1/2)


def test_compute_bully_factor(analyzer):
    actions = [
        ActionEvent(player="BB", action="bet", street="flop", amount=None, timestamp=None, target="hero"),
        ActionEvent(player="BB", action="raise", street="turn", amount=None, timestamp=None, target="hero"),
        ActionEvent(player="BB", action="bet", street="river", amount=None, timestamp=None, target="villain2"),
    ]
    hand = HandActionHistory(hand_id="h7", actions=actions)
    history = VillainActionHistory(seat="BB", total_hands_played=1, hands=[hand])
    result = analyzer.analyze(history)
    assert result["villain_hero_bully_history"] == pytest.approx(2/2)
