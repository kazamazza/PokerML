from analysis.action_history_analyzer import ActionHistoryAnalyzer
from analysis.position_analyzer import PositionAnalyzer
from board_analyzer import BoardAnalyzer
from eval7_service import Eval7Service
from hand_classifier.hand_classifier import HandClassifier
from models.poker_ml_input import PokerMLInput, PositionContext, Tier1Inputs, Tier2Inputs
from models.poker_session import PokerSession
from models.villain_action_history import VillainActionHistory, HandActionHistory
from villain_range_estimator import VillainRangeEstimator


class InputVectorBuilder:
    def __init__(
        self,
        eval_service: Eval7Service,
        hand_classifier: HandClassifier,
        board_analyzer: BoardAnalyzer,
        villain_estimator: VillainRangeEstimator,
        position_analyzer: PositionAnalyzer,
        action_history_analyzer: ActionHistoryAnalyzer
    ):
        self.eval_service = eval_service
        self.hand_classifier = hand_classifier
        self.board_analyzer = board_analyzer
        self.villain_estimator = villain_estimator
        self.position_analyzer = position_analyzer
        self.action_history_analyzer = action_history_analyzer

    def build(self, session: PokerSession) -> PokerMLInput:
        # 1. Tier 1 base extraction
        hero_hand = session.hero_hand.strip().replace(" ", "")
        board = session.board.split(",") if session.board else []
        street = session.street
        pot_size = session.pot_size or 0.0
        stack = session.stack_sizes.get(session.hero_position, 0.0)
        spr = stack / pot_size if pot_size > 0 else 0.0
        role = self._infer_player_role(session)

        # 2. Derived fields
        board_texture = self.board_analyzer.analyze(board)
        hand_strength = self.hand_classifier.classify(hero_hand, board)
        equity = self.eval_service.calculate_equity(hero_hand, board, villain_range=...)  # dynamic villain range

        # 3. Position context
        position_ctx = self.position_analyzer.analyze(session)

        tier1 = Tier1Inputs(
            hero_hand=hero_hand,
            board_cards=board,
            street=street,
            hero_position=session.heroPosition,
            player_role=role,
            stack_to_pot_ratio=spr,
            pot_size=pot_size,
            effective_stack=stack,
            legal_actions=[...],
            hero_equity_vs_range=equity,
            hero_hand_strength=hand_strength.label,  # ✅ just the label
            board_texture=board_texture,  # ✅ just the structure string
            position_context=position_ctx
        )

        hero = session.hero_position
        active_villains = [
            s.seat_id for s in session.seats
            if s.seat_id != hero and s.seat_id not in session.folded_players
        ]

        tier2_aggregate = {}

        for seat in active_villains:
            villain_actions = [a for a in session.action_history if a.player == seat]

            hand_history = HandActionHistory(hand_id=session.current_hand_id, actions=villain_actions)

            history = VillainActionHistory(
                seat=seat,
                total_hands_played=1,
                hands=[hand_history],
            )

            stats = self.action_history_analyzer.analyze(history)

            for k, v in stats.items():
                tier2_aggregate.setdefault(k, []).append(v)

        tier2_averaged = {k: sum(vs) / len(vs) for k, vs in tier2_aggregate.items()}
        tier2 = Tier2Inputs(**tier2_averaged)
        tier3 = ...

        return PokerMLInput(tier1=tier1, tier2=tier2, tier3=tier3)

    def _infer_player_role(self, session: PokerSession) -> str:
        hero_pos = session.hero_position
        player_count = session.player_count
        folded = set(session.folded_players or [])

        # Remaining players
        active_seats = [seat for seat in session.stack_sizes.keys() if seat not in folded]

        # Heads-up roles
        if player_count == 2:
            if hero_pos == "BTN":
                return "BTN_vs_BB"
            elif hero_pos == "BB":
                return "BB_vs_BTN"
            else:
                return f"{hero_pos}_vs_other"

        # 6-max or full ring roles
        if player_count >= 3:
            remaining = len(active_seats)
            if remaining == 2:
                villain_pos = next(seat for seat in active_seats if seat != hero_pos)
                return f"{hero_pos}_vs_{villain_pos}"
            else:
                return f"{hero_pos}_vs_Multiway"

        # Fallback
        return f"{hero_pos}_unknown"