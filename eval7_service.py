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

        hero_hand_strength = 0
        total = 0

        for villain_str in villain_range:
            villain = [eval7.Card(villain_str[:2]), eval7.Card(villain_str[2:])]

            if set(hero + villain + board_cards) != len(set(hero + villain + board_cards)):
                continue  # skip illegal combos with overlapping cards

            hero_score = 0
            for _ in range(self.iterations):
                deck = eval7.Deck()
                # remove known cards
                for card in hero + villain + board_cards:
                    deck.cards.remove(card)

                remaining_board = list(board_cards)
                while len(remaining_board) < 5:
                    remaining_board.append(deck.deal(1)[0])

                hero_eval = eval7.evaluate(hero + remaining_board)
                villain_eval = eval7.evaluate(villain + remaining_board)

                if hero_eval > villain_eval:
                    hero_score += 1
                elif hero_eval == villain_eval:
                    hero_score += 0.5

            total += self.iterations
            hero_hand_strength += hero_score

        return hero_hand_strength / total if total > 0 else 0.0