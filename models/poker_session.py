from enum import Enum

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

class PlayerRole(str, Enum):
    UTG_vs_BB = "UTG_vs_BB"
    MP_vs_BB = "MP_vs_BB"
    CO_vs_BB = "CO_vs_BB"
    BTN_vs_BB = "BTN_vs_BB"
    SB_vs_BB = "SB_vs_BB"
    BTN_vs_SB_vs_BB = "BTN_vs_SB_vs_BB"
    ThreeBetPot = "ThreeBetPot"
    SRP_vs_Limper = "SRP_vs_Limper"
    HeadsUp = "HeadsUp"
    Multiway = "Multiway"
    UTG_vs_CO = "UTG_vs_CO"
    MP_vs_BTN = "MP_vs_BTN"
    CO_vs_BTN = "CO_vs_BTN"
    SB_vs_UTG = "SB_vs_UTG"
    BB_vs_SB = "BB_vs_SB"
    BTN_vs_CO = "BTN_vs_CO"

class PokerSession(BaseModel):
    session_id: str
    current_hand_id: str
    hero_id: str
    stakes: Stakes
    hero_hand: str                      # e.g., "AhKd"
    board: Optional[str] = None         # e.g., "7hTdQs" or None (preflop)
    street: Street
    pot_size: float
    player_count: int

    stack_sizes: Dict[TableSeat, float]         # e.g., {"BTN": 100.0, "CO": 80.0}
    hero_position: TableSeat
    folded_players: List[TableSeat]
    seats: List[PlayerSeat]                     # Who's at the table, incl. seatId and playerId
    action_history: List[ActionEvent]           # Complete history of hand

    past_hand_results: Optional[List[HandResult]] = None  # Optional historical context

    player_role: PlayerRole  # ✅ NEW: direct from Node backend