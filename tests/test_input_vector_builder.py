import pytest

from container import Container
from models.poker_ml_input import GameDynamics, PsychologicalContext, PokerMLInput, FundamentalInputs
from models.poker_session import Stakes, PlayerSeat, ActionEvent, PokerSession, PlayerRole


@pytest.fixture
def container(monkeypatch):
    c = Container()
    # Patch out the real equity service with a fast stub
    c.eval_service.iterations = 1
    monkeypatch.setattr(c.eval_service, "calculate_equity", lambda hero_hand, board, villain_range: 0.123)
    return c

@pytest.fixture
def session():
    stakes = Stakes(big_blind=2.0, small_blind=1.0)
    seats = [
        PlayerSeat(seat_id="BTN", player_id="hero", stack_size=100.0),
        PlayerSeat(seat_id="BB",  player_id="villain", stack_size=80.0),
    ]
    action_history = [
        ActionEvent(player="BB", action="bet", amount=2.0, street="flop", timestamp=1),
        ActionEvent(player="hero", action="call", amount=2.0, street="flop", timestamp=2),
    ]
    return PokerSession(
        session_id="sess1",
        current_hand_id="hand1",
        hero_id="hero",
        stakes=stakes,
        hero_hand=["Ah", "Kd"],
        board=["As", "9d", "2c"],
        street="flop",
        pot_size=6.0,
        player_count=2,
        stack_sizes={"BTN": 100.0, "BB": 80.0},
        hero_position="BTN",
        folded_players=[],
        seats=seats,
        action_history=action_history,
        past_hand_results=[],
        player_role=PlayerRole.BTN_vs_BB,
    )

def test_full_input_vector_pipeline(container, session):
    builder = container.input_vector_builder
    ml_input: PokerMLInput = builder.build(session)

    # Basic sanity checks
    assert isinstance(ml_input, PokerMLInput)

    # Fundamentals
    f: FundamentalInputs = ml_input.fundamentals
    assert f.hero_hand == ["Ah", "Kd"]
    assert f.board_cards == ["As", "9d", "2c"]
    assert f.street == "flop"
    assert pytest.approx(f.stack_to_pot_ratio) == 100.0/6.0
    assert f.legal_actions  # non-empty list
    # equity was stubbed to 0.123
    assert pytest.approx(f.hero_equity_vs_range, rel=1e-3) == 0.123

    # Dynamics
    dyn: GameDynamics = ml_input.dynamics
    assert dyn.session_heat in {"hot","cold","neutral"}
    assert dyn.hero_tilt_state in {"tilted","careful","neutral"}

    # Psych
    psych: PsychologicalContext = ml_input.psych
    assert psych.board_cluster_key is not None
    assert 0.0 <= (psych.multiway_aggression_score or 0) <= 1.0

    # Villain profiles present for BB
    assert "BB" in ml_input.villain_profiles
    vp = ml_input.villain_profiles["BB"]
    # check a few numeric metrics exist
    assert hasattr(vp, "vpip")
    assert hasattr(vp, "pfr")
    assert hasattr(vp, "overall_winrate")