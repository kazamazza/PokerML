from pydantic import BaseModel
from typing import List
from models.poker_session import TableSeat, ActionEvent


class HandActionHistory(BaseModel):
    hand_id: str
    actions: List[ActionEvent]

class VillainActionHistory(BaseModel):
    seat: TableSeat
    total_hands_played: int
    hands: List[HandActionHistory]