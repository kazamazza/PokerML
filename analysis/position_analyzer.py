from typing import List, Optional
from models.poker_ml_input import PositionContext
from models.poker_session import PokerSession, TableSeat

class PositionAnalyzer:
    def __init__(self):
        pass

    def analyze(self, session: PokerSession) -> PositionContext:
        hero_position: TableSeat = session.hero_position
        all_seats: List[TableSeat] = list(session.stack_sizes.keys())
        active_seats = [seat for seat in all_seats if seat not in session.folded_players]
        villain_positions = [seat for seat in active_seats if seat != hero_position]

        is_heads_up = len(villain_positions) == 1
        is_multiway = len(villain_positions) > 1
        in_position = self._is_in_position(hero_position, villain_positions, all_seats)

        # Determine last aggressor: prefer session.calculations if available, else scan action_history
        aggressor_position: Optional[str] = None
        if hasattr(session, 'calculations') and session.calculations and getattr(session.calculations, 'lastAggressor', None):
            aggressor_position = session.calculations.lastAggressor
        else:
            for event in reversed(session.action_history):
                if event.action in {'bet', 'raise', '3bet', 'shove', 'check_raise'}:
                    aggressor_position = event.player  # assuming player holds the seat identifier
                    break

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

        total_players = len(seat_order)
        hero_idx = seat_order.index(hero)
        villain_indices = [seat_order.index(v) for v in villains]

        # Hero is in position if all villains act before hero in the circular order
        for i in range(1, total_players):
            next_idx = (hero_idx + i) % total_players
            if next_idx in villain_indices:
                return False  # someone acts after hero

        return True
