from dataclasses import dataclass, asdict
from typing import List, Optional, Literal, Dict
from pydantic import BaseModel
from models.board_texture import BoardTexture


@dataclass
class PositionContext:
    in_position: bool
    is_heads_up: bool
    is_multiway: bool
    aggressor_position: str

class BetAction(BaseModel):
    player: str
    action: str
    size: float

@dataclass
class VillainProfile:
    seat_id: str
    profile_type: Literal["tight", "loose", "aggressive", "passive", "unknown"]
    vpip: float
    pfr: float
    aggression_factor: float
    bluff_frequency: float
    check_raise_frequency: float
    showdown_winrate: float
    cold_call_frequency: float
    hero_bully_history: float
    hero_vs_villain_winrate: float
    snap_action_frequency: float
    emotional_tilt_level: Literal["calm", "neutral", "tilted"]
    collusion_risk: Literal["low", "medium", "high"]
    overall_winrate: float
    line_pattern: str

    def to_dict(self) -> dict:
        return asdict(self)

@dataclass
class PsychologicalContext:
    hero_recent_big_loss_flag: Optional[bool]
    multiway_aggression_score: Optional[float]
    board_cluster_key: Optional[str]

@dataclass
class GameDynamics:
    bet_history: Optional[List[BetAction]]
    hero_tilt_state: Optional[Literal["tilted", "confident", "careful", "neutral"]]
    session_heat: Optional[Literal["hot", "cold", "neutral"]]

@dataclass
class FundamentalInputs:
    hero_hand: List[str]                           # e.g. "AhKd"
    board_cards: List[str]                  # e.g. ["As", "9d", "2c"]
    street: Literal["preflop", "flop", "turn", "river"]
    hero_position: str                      # e.g. "BTN"
    player_role: str                        # e.g. "BTN_vs_BB"
    stack_to_pot_ratio: float
    pot_size: float
    effective_stack: float
    legal_actions: List[str]                # e.g. ["fold", "call", "raise_50"]
    hero_equity_vs_range: float            # 0.0 – 1.0
    hero_hand_strength: str                # e.g. "top_pair", "combo_draw", etc.
    board_texture: BoardTexture
    position_context: PositionContext


@dataclass
class PokerMLInput:
    fundamentals: FundamentalInputs
    villain_profiles: Dict[str, VillainProfile]  # seat → profile
    dynamics: GameDynamics
    psych: PsychologicalContext