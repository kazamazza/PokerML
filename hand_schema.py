from typing import List, Dict, Optional
from pydantic import BaseModel

class HandHistory(BaseModel):
    hand_id: Optional[str]
    street: Optional[str]  # Optional during normalization
    hole_cards_by_player: Dict[str, List[str]]
    board: List[str]
    actions: List[str]
    players: List[str]
    winnings: List  # can be refined later
    min_bet: float
    stakes: str