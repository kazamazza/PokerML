import pytest

from container import Container
from features.input_vector_builder import InputVectorBuilder
from models.poker_ml_input import FundamentalInputs
from models.poker_session import PokerSession


# Static sample JSON input
@pytest.fixture
def sample_session_json():
    return {
        "session_id": "abc123",
        "current_hand_id": "hand001",
        "hero_id": "hero1",
        "stakes": {
            "big_blind": 2.0,
            "small_blind": 1.0
        },
        "hero_hand": "AhKd",
        "board": "As9d2c",
        "street": "flop",
        "pot_size": 6.0,
        "player_count": 2,
        "stack_sizes": {
            "BTN": 100.0,
            "BB": 80.0
        },
        "hero_position": "BTN",
        "folded_players": [],
        "seats": [
            {"seat_id": "BTN", "player_id": "hero1", "stack_size": 100.0},
            {"seat_id": "BB", "player_id": "villain1", "stack_size": 80.0}
        ],
        "action_history": [
            {
                "player": "villain1",
                "action": "check",
                "amount": None,
                "street": "flop",
                "timestamp": 1
            },
            {
                "player": "hero1",
                "action": "bet",
                "amount": 3.0,
                "street": "flop",
                "timestamp": 2
            }
        ],
        "past_hand_results": [],
        "player_role": "BTN_vs_BB"
    }


def test_build_tier1_inputs_from_json(sample_session_json):
    # Parse session from raw JSON
    session = PokerSession.from_json(sample_session_json)
    # Build Tier 1 inputs
    container = Container()
    builder: InputVectorBuilder = container.input_vector_builder
    inputs = builder.build(session)

    assert isinstance(inputs.fundamentals, FundamentalInputs)

    # Check some core values
    assert inputs.fundamentals.hero_hand == ["Ah", "Kd"]
    assert inputs.fundamentals.board_cards == ["As", "9d", "2c"]
    assert inputs.fundamentals.street == "flop"
    assert inputs.fundamentals.hero_position == "BTN"
    assert inputs.fundamentals.player_role == "BTN_vs_BB"
    assert inputs.fundamentals.stack_to_pot_ratio > 0
    assert 0 <= inputs.fundamentals.hero_equity_vs_range <= 1
    assert isinstance(inputs.fundamentals.board_texture.suits, dict)
    assert "call" in inputs.fundamentals.legal_actions