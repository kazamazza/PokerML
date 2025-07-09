from models.poker_session import PokerSession, TableSeat

class PositionAnalyzer:
    def __init__(self):
        pass

    def analyze(self, session: PokerSession) -> dict:
        """
        Derive positional context from hero and villain seat positions.
        """
        hero_position = session.heroPosition
        villain_positions = [
            seat for seat in session.stackSizes.keys()
            if seat != hero_position and seat not in session.foldedPlayers
        ]

        is_heads_up = len(villain_positions) == 1
        is_multiway = len(villain_positions) > 1

        # Basic heuristic for in-position
        ip = self._is_in_position(hero_position, villain_positions)

        # Placeholder: aggressor logic
        aggressor_position = session.calculations.lastAggressor if session.calculations else None

        return {
            "hero_position": hero_position,
            "villain_positions": villain_positions,
            "in_position": ip,
            "is_heads_up": is_heads_up,
            "is_multiway": is_multiway,
            "aggressor_position": aggressor_position
        }

    def _is_in_position(self, hero: TableSeat, villains: list) -> bool:
        """
        Placeholder IP logic. Real logic would involve seat ordering.
        """
        return True if hero == "BTN" else False  # Simplified