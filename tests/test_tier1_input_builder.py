from typing import List

import pytest

from container import Container
from features.input_vector_builder import InputVectorBuilder
from models.hand_result import HandResult
from models.poker_session import PokerSession, Street, TableSeat, Stakes, PlayerSeat, ActionEvent, PlayerRole


class MockSession(PokerSession):
    session_id: str = "abc123"
    current_hand_id: str = "hand001"
    hero_id: str = "hero1"
    stakes: Stakes = Stakes(big_blind=2.0, small_blind=1.0)
    hero_hand: str = "AhKd"
    board: str = "As9d2c"
    street: Street = Street.FLOP
    pot_size: float = 6.0
    player_count: int = 2
    stack_sizes: dict = {
        TableSeat.BTN: 100.0,
        TableSeat.BB: 80.0
    }
    hero_position: TableSeat = TableSeat.BTN
    folded_players: List[TableSeat] = []
    seats: List[PlayerSeat] = [
        PlayerSeat(seat_id=TableSeat.BTN, player_id="hero1"),
        PlayerSeat(seat_id=TableSeat.BB, player_id="villain1")
    ]
    action_history: List[ActionEvent] = [
        ActionEvent(player="villain1", action="check", amount=None, street=Street.FLOP, timestamp=1),
        ActionEvent(player="hero1", action="bet", amount=3.0, street=Street.FLOP, timestamp=2),
    ]
    past_hand_results: List[HandResult] = []
    player_role: PlayerRole = PlayerRole.BTN_vs_BB


@pytest.fixture
def tier1_inputs():
    container = Container()
    session = MockSession()
    builder: InputVectorBuilder = container.input_vector_builder  # Injected with full dependencies
    return builder.build(session)


def test_hero_hand(tier1_inputs):
    assert tier1_inputs.hero_hand == "AhKd"


def test_board_cards(tier1_inputs):
    assert tier1_inputs.board_cards == ["As", "9d", "2c"]


def test_street(tier1_inputs):
    assert tier1_inputs.street == "flop"


def test_hero_position(tier1_inputs):
    assert tier1_inputs.hero_position == "BTN"


def test_player_role(tier1_inputs):
    assert tier1_inputs.player_role == "BTN_vs_BB"


def test_stack_to_pot_ratio(tier1_inputs):
    assert isinstance(tier1_inputs.stack_to_pot_ratio, float)


def test_pot_size(tier1_inputs):
    assert tier1_inputs.pot_size == 6.0


def test_effective_stack(tier1_inputs):
    assert isinstance(tier1_inputs.effective_stack, float)
    assert tier1_inputs.effective_stack == 80.0  # min(hero, villain)


def test_legal_actions(tier1_inputs):
    assert isinstance(tier1_inputs.legal_actions, list)
    assert all(isinstance(a, str) for a in tier1_inputs.legal_actions)


def test_hero_equity_vs_range(tier1_inputs):
    assert 0.0 <= tier1_inputs.hero_equity_vs_range <= 1.0


def test_hero_hand_strength(tier1_inputs):
    assert isinstance(tier1_inputs.hero_hand_strength, str)


def test_board_texture(tier1_inputs):
    assert hasattr(tier1_inputs.board_texture, "structure")
    assert tier1_inputs.board_texture.structure in ["paired", "connected", "uncoordinated"]


def test_position_context(tier1_inputs):
    ctx = tier1_inputs.position_context
    assert isinstance(ctx.in_position, bool)
    assert isinstance(ctx.is_heads_up, bool)
    assert isinstance(ctx.is_multiway, bool)
    assert isinstance(ctx.aggressor_position, str)