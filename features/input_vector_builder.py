from analysis.action_history_analyzer import ActionHistoryAnalyzer
from analysis.position_analyzer import PositionAnalyzer
from analysis.psychological_analyzer import PsychologicalAnalyzer
from board_analyzer import BoardAnalyzer
from eval7_service import Eval7Service
from hand_classifier.hand_classifier import HandClassifier
from helper.hand_range_utils import HandRangeUtils
from helper.legal_action_resolver import LegalActionResolver
from helper.role_position_parser import RolePositionParser
from models.poker_ml_input import PokerMLInput, Tier1Inputs, Tier2Inputs, Tier3Inputs, BetAction
from models.poker_session import PokerSession
from models.villain_action_history import VillainActionHistory, HandActionHistory
from services.hand_range_service import HandRangeService
from villain_range_estimator import VillainRangeEstimator


class InputVectorBuilder:
    def __init__(
        self,
        eval_service: Eval7Service,
        hand_classifier: HandClassifier,
        board_analyzer: BoardAnalyzer,
        villain_estimator: VillainRangeEstimator,
        position_analyzer: PositionAnalyzer,
        action_history_analyzer: ActionHistoryAnalyzer,
        psychological_analyzer: PsychologicalAnalyzer,
        hand_range_service: HandRangeService,
        legal_action_resolver: LegalActionResolver,

    ):
        self.eval_service = eval_service
        self.hand_classifier = hand_classifier
        self.board_analyzer = board_analyzer
        self.villain_estimator = villain_estimator
        self.position_analyzer = position_analyzer
        self.action_history_analyzer = action_history_analyzer
        self.psychological_analyzer = psychological_analyzer
        self.hand_range_service = hand_range_service
        self.legal_action_resolver = legal_action_resolver

    def build(self, session: PokerSession) -> PokerMLInput:
        # 1. Tier 1 base extraction
        hero_hand = session.hero_hand.strip().replace(" ", "")
        board = session.board.split(",") if session.board else []
        street = session.street
        pot_size = session.pot_size or 0.0
        stack = session.stack_sizes.get(session.hero_position, 0.0)
        spr = stack / pot_size if pot_size > 0 else 0.0

        role = session.role

        # 1. Derived fields
        board_texture = self.board_analyzer.analyze(board)
        hand_strength = self.hand_classifier.classify(hero_hand, board)

        # 2. Determine hero and villains based on role
        parser = RolePositionParser(role)
        hero_pos = parser.get_hero()
        villain_positions = parser.get_villains()

        # 3. Load villain hand ranges
        villain_ranges = []

        for villain_pos in villain_positions:
            villain_range = self.hand_range_service.get_range(
                player_role=role,
                round=street,
                board=board,
            )
            if villain_range:
                villain_ranges.append(villain_range)

        # 4. Combine villain ranges for Eval7 (e.g., union of combos)
        combined_villain_range = HandRangeUtils.merge_ranges(villain_ranges)

        # 5. Run equity calculation
        equity = self.eval_service.calculate_equity(
            hero_hand=hero_hand,
            board=board,
            villain_range=combined_villain_range
        )
        # 3. Position context
        position_ctx = self.position_analyzer.analyze(session)

        legal_actions = self.legal_action_resolver.resolve(
            street=street,
            stack=stack,
            pot_size=pot_size,
            bet_history=[
                BetAction(player=a.player, action=a.action, size=a.amount or 0.0)
                for a in session.action_history
                if a.action in {"bet", "raise", "call", "3bet", "shove"}
            ],
            is_all_in=session.hero_profile.isAllIn
        )

        tier1 = Tier1Inputs(
            hero_hand=hero_hand,
            board_cards=board,
            street=street,
            hero_position=session.heroPosition,
            player_role=role,
            stack_to_pot_ratio=spr,
            pot_size=pot_size,
            effective_stack=stack,
            legal_actions=legal_actions,
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
        # Tier 3 psychological metrics
        tier3_metrics = self.psychological_analyzer.analyze(session)
        tier3 = Tier3Inputs(**tier3_metrics)

        return PokerMLInput(tier1=tier1, tier2=tier2, tier3=tier3)