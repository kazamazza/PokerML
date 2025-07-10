from typing import List

class PostflopRangeRefiner:
    STRAIGHT_RANKS = "23456789TJQKA"

    def refine(self, base_range: List[str], board: List[str]) -> List[str]:
        if not base_range:
            return ["AA", "KK", "QQ"]

        ranks_on_board = {card[0] for card in board}
        suits_on_board = {}
        for card in board:
            suit = card[1]
            suits_on_board[suit] = suits_on_board.get(suit, 0) + 1

        flush_suit = next((suit for suit, count in suits_on_board.items() if count >= 3), None)

        board_ranks_idx = [self.STRAIGHT_RANKS.index(r) for r in ranks_on_board if r in self.STRAIGHT_RANKS]
        max_board_rank = max(board_ranks_idx, default=0)
        min_board_rank = min(board_ranks_idx, default=0)

        is_paired_board = any(
            board[i][0] == board[j][0]
            for i in range(len(board))
            for j in range(i + 1, len(board))
        )
        is_wet_board = flush_suit is not None or (max_board_rank - min_board_rank <= 4)

        refined = []
        for hand in base_range:
            rank1, rank2 = hand[:2]
            suited = hand.endswith("s")

            if suited and flush_suit:
                refined.append(hand)
                continue

            is_connector = abs(self.STRAIGHT_RANKS.index(rank1) - self.STRAIGHT_RANKS.index(rank2)) == 1
            is_one_gapper = abs(self.STRAIGHT_RANKS.index(rank1) - self.STRAIGHT_RANKS.index(rank2)) == 2

            if suited and is_connector and flush_suit:
                refined.append(hand)
                continue
            if suited and is_one_gapper:
                refined.append(hand)
                continue

            if rank1 not in ranks_on_board or rank2 not in ranks_on_board:
                refined.append(hand)
                continue

            hand_ranks = [self.STRAIGHT_RANKS.index(rank1), self.STRAIGHT_RANKS.index(rank2)]
            if min(hand_ranks) > max_board_rank:
                refined.append(hand)
                continue

        if is_paired_board:
            refined = [h for h in refined if any(high in h for high in ["A", "K", "Q", "J", "T"])]

        if is_wet_board:
            refined = [h for h in refined if h.endswith("s") or any(high in h for high in ["A", "K"])]

        return refined if refined else base_range