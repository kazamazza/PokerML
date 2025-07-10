from typing import List, Optional, Literal, Dict
from pydantic import BaseModel, Field

from models.board_texture import BoardTexture


# TIER 1 — Essential Inputs
class PositionContext(BaseModel):
    in_position: bool
    is_heads_up: bool
    is_multiway: bool
    aggressor_position: str


class Tier1Inputs(BaseModel):
    hero_hand: str                           # e.g. "AhKd"
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


# TIER 2 — Intermediate Game Dynamics
class BetAction(BaseModel):
    player: str
    action: str
    size: float


class Tier2Inputs(BaseModel):
    villain_profile_type: Optional[Literal["tight", "loose", "aggressive", "passive", "unknown"]]
    villain_vpip: Optional[float]
    villain_pfr: Optional[float]
    villain_aggression_factor: Optional[float]
    villain_bluff_frequency: Optional[float]
    villain_check_raise_freq: Optional[float]
    villain_showdown_winrate: Optional[float]
    hero_tilt_state: Optional[Literal["tilted", "confident", "careful", "neutral"]]
    session_heat: Optional[Literal["hot", "cold", "neutral"]]
    bet_history: Optional[List[BetAction]]
    villain_cold_call_frequency: Optional[float]
    villain_hero_bully_history: Optional[float]


# TIER 3 — Deep Psychology / Meta
class Tier3Inputs(BaseModel):
    hero_vs_villain_winrate: Optional[float]
    hero_recent_big_loss_flag: Optional[bool]
    villain_snap_action_freq: Optional[float]
    villain_emotional_tilt_level: Optional[Literal["calm", "neutral", "tilted"]]
    multiway_aggression_score: Optional[float]
    board_cluster_key: Optional[str]
    villain_line_pattern: Optional[str]
    villain_collusion_risk_level: Optional[Literal["low", "medium", "high"]]
    villain_overall_winrate: Optional[float]


# FULL MODEL
class PokerMLInput(BaseModel):
    tier1: Tier1Inputs
    tier2: Optional[Tier2Inputs] = None
    tier3: Optional[Tier3Inputs] = None