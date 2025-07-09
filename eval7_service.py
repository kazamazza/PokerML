import eval7
from typing import List


class Eval7Service:
    def __init__(self, iterations: int = 1000):
        self.iterations = iterations

    def calculate_equity(self, hero_hand: str, board: List[str], villain_range: List[str]) -> float:
        """
        Estimate hero equity vs a villain range using eval7 Monte Carlo.

        Args:
            hero_hand: e.g., "AhKs"
            board: e.g., ["Ad", "7c", "2h"]
            villain_range: list of combos like ["QcJc", "9h9d", ...]

        Returns:
            equity (float): between 0 and 1
        """
        hero = [eval7.Card(hero_hand[:2]), eval7.Card(hero_hand[2:])]
        board_cards = [eval7.Card(card) for card in board]

        hero_wins = 0
        total_runs = 0

        known_cards = set(hero + board_cards)

        for villain_str in villain_range:
            villain = [eval7.Card(villain_str[:2]), eval7.Card(villain_str[2:])]

            # Skip combos with overlapping cards
            if len(set(hero + villain + board_cards)) != len(hero + villain + board_cards):
                continue

            deck = eval7.Deck()
            for card in hero + villain + board_cards:
                deck.cards.remove(card)

            for _ in range(self.iterations):
                deck.shuffle()
                full_board = board_cards.copy()
                while len(full_board) < 5:
                    full_board.append(deck.peek())

                hero_eval = eval7.evaluate(hero + full_board)
                villain_eval = eval7.evaluate(villain + full_board)

                if hero_eval < villain_eval:  # lower = better hand
                    hero_wins += 1
                elif hero_eval == villain_eval:
                    hero_wins += 0.5
                # else villain wins (score += 0)

                total_runs += 1

        return hero_wins / total_runs if total_runs > 0 else 0.0