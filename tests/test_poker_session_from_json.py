import pytest

from models.poker_session import PokerSession


@pytest.fixture
def sample_session_json():
    return  {
    "session_id": "abc123",
    "current_hand_id": "hand001",
    "hero_id": "hero1",
    "stakes": {
        "big_blind": 2,
        "small_blind": 1
    },
    "hero_hand": "AhKd",
    "board": "As9d2c",  # 🟢 Changed from list to string
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
        {"seat_id": "BTN", "player_id": "hero1", "stack_size": 100.0},  # 🟢 fixed
        {"seat_id": "BB", "player_id": "villain1", "stack_size": 80.0}  # 🟢 fixed
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
    "player_role": "BTN_vs_BB"
}

def test_poker_session_from_json(sample_session_json):
    session = PokerSession.from_json(sample_session_json)

    assert session.session_id == "abc123"
    assert session.hero_hand == "AhKd"
    assert session.board == "As9d2c"
    assert session.street == "flop"
    assert session.stakes.big_blind == 2.0
    assert session.stakes.small_blind == 1.0
    assert session.hero_position == "BTN"
    assert session.stack_sizes["BB"] == 80.0
    assert len(session.seats) == 2
    assert session.action_history[0].action == "check"
    assert session.player_role == "BTN_vs_BB"