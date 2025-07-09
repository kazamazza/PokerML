# hh_normalizer.py

from typing import Dict, Any, List
from hand_schema import HandHistory


def normalize_parsed_hand(raw_hand: Dict[str, Any]) -> Dict:
    """
    Transforms any vendor-specific parsed hand into your canonical HandHistory format.
    """
    # Normalize players list
    players = raw_hand.get("players", [])
    if isinstance(players, str):  # some parsers may return comma-separated string
        players = [p.strip() for p in players.split(",")]

    return HandHistory(
        hand_id=raw_hand.get("hand_id"),
        street=raw_hand.get("street"),
        hole_cards_by_player=raw_hand.get("hole_cards_by_player", {}),
        board=raw_hand.get("board", []),
        actions=raw_hand.get("actions", []),
        players=players,
        winnings=raw_hand.get("winnings", []),
        min_bet=float(raw_hand.get("min_bet", 0)),
        stakes=raw_hand.get("stakes", "NL10"),
    ).dict()