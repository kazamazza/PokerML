from typing import List
from models.poker_ml_input import BetAction
from models.poker_session import Street


class LegalActionResolver:
    def resolve(
        self,
        street: Street,
        stack: float,
        pot_size: float,
        bet_history: List[BetAction],
        is_all_in: bool = False
    ) -> List[str]:
        if is_all_in:
            return ["check"]  # or [] depending on context

        legal_actions = {"fold", "call", "raise"}

        if street == "preflop" and not any(b.action == "raise" for b in bet_history):
            legal_actions.add("limp")

        # Example logic — refine this per game rules
        raise_sizes = [0.5 * pot_size, pot_size]
        legal_actions.update([f"raise_{int(size)}" for size in raise_sizes if size < stack])

        return sorted(legal_actions)