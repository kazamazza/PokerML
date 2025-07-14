import random
import eval7
from typing import List


class Eval7Service:
    def __init__(self, iterations: int = 1000):
        self.iterations = iterations

    def calculate_equity(self, hero_hand: List[str], board: List[str], villain_range: List[str]) -> float:
        hero = [eval7.Card(card) for card in hero_hand]
        board_cards = [eval7.Card(card) for card in board]

        hero_wins = 0
        total_runs = 0

        for villain_str in villain_range:
            if len(villain_str) != 4:
                continue  # skip invalid combo

            try:
                villain = [eval7.Card(villain_str[:2]), eval7.Card(villain_str[2:])]
            except Exception:
                continue  # skip bad strings like "XZXX"

            # Skip combos with overlapping cards
            if len(set(hero + villain + board_cards)) != len(hero + villain + board_cards):
                continue

            # Build deck excluding known cards
            full_deck = [card for card in eval7.Deck() if card not in hero + villain + board_cards]

            for _ in range(self.iterations):
                eval_deck = full_deck.copy()
                random.shuffle(eval_deck)

                full_board = board_cards.copy()
                while len(full_board) < 5:
                    full_board.append(eval_deck.pop())

                hero_eval = eval7.evaluate(hero + full_board)
                villain_eval = eval7.evaluate(villain + full_board)

                if hero_eval < villain_eval:
                    hero_wins += 1
                elif hero_eval == villain_eval:
                    hero_wins += 0.5

                total_runs += 1

        return hero_wins / total_runs if total_runs > 0 else 0.0