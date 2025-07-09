from typing import List
from models.poker_ml_input import PositionContext
from models.poker_session import PokerSession, TableSeat

class PositionAnalyzer:
    def __init__(self):
        pass

    def analyze(self, session: PokerSession) -> PositionContext:
        hero_position: TableSeat = session.heroPosition
        all_seats: List[TableSeat] = list(session.stackSizes.keys())
        active_seats = [seat for seat in all_seats if seat not in session.foldedPlayers]
        villain_positions = [seat for seat in active_seats if seat != hero_position]

        is_heads_up = len(villain_positions) == 1
        is_multiway = len(villain_positions) > 1
        in_position = self._is_in_position(hero_position, villain_positions, all_seats)

        # Estimate aggressor
        aggressor_position = (
            session.calculations.lastAggressor if session.calculations else None
        )
        if not aggressor_position and session.lastAggressiveAction:
            aggressor_position = session.lastAggressiveAction.playerSeat

        return PositionContext(
            in_position=in_position,
            is_heads_up=is_heads_up,
            is_multiway=is_multiway,
            aggressor_position=aggressor_position,
        )

    def _is_in_position(
        self, hero: TableSeat, villains: List[TableSeat], seat_order: List[TableSeat]
    ) -> bool:
        """
        Determines whether hero is last to act on postflop streets.
        Seat order is used to infer action flow clockwise.
        """
        if not villains:
            return True  # solo player

        # Create circular index map
        total_players = len(seat_order)
        hero_idx = seat_order.index(hero)
        villain_indices = [seat_order.index(v) for v in villains]

        # Find first actor (smallest index after hero)
        # In poker, postflop acts left of button → circular comparison
        # So hero is in position if their index is higher than all villains (modulo wraparound)
        for i in range(1, total_players):
            next_idx = (hero_idx + i) % total_players
            if next_idx in villain_indices:
                return False  # someone acts after hero

        return True