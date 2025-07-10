from pydantic import BaseModel


class HandResult(BaseModel):
    hand_id: str
    hero_id: str
    villain_id: str
    hero_won: bool
    net_bb: float  # Hero's profit/loss in big blinds