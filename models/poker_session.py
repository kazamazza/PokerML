from pydantic import BaseModel
from typing import List, Dict, Literal, Optional

from models.hand_result import HandResult

Street = Literal["preflop", "flop", "turn", "river"]
TableSeat = Literal["BTN", "CO", "MP", "UTG", "SB", "BB"]  # Extend if more positions are used

class ActionEvent(BaseModel):
    player: str  # playerId or seat
    action: str  # "fold", "call", "raise", etc.
    amount: Optional[float] = None
    street: Street
    timestamp: Optional[int] = None
    target: Optional[str] = None  # 🆕 Add this if tracking targeted aggression

class Stakes(BaseModel):
    big_blind: float
    small_blind: float

class PlayerSeat(BaseModel):
    seat_id: TableSeat
    player_id: str
    stack_size: float

class PokerSession(BaseModel):
    session_id: str
    current_hand_id: str
    hero_id: str
    stakes: Stakes
    hero_hand: str                  # e.g. "AhKd"
    board: Optional[str]           # e.g. "7hTdQs", can be None for preflop
    street: Street
    pot_size: float
    player_count: int
    stack_sizes: Dict[TableSeat, float]  # e.g. {"BTN": 100, "CO": 80, ...}
    hero_position: TableSeat
    folded_players: List[TableSeat]
    seats: List[PlayerSeat]
    action_history: List[ActionEvent]
    past_hand_results: Optional[List[HandResult]] = None