from typing import Dict
from analysis.position_analyzer import PositionAnalyzer
from board_analyzer import BoardAnalyzer
from eval7_service import Eval7Service
from hand_classifier.hand_classifier import HandClassifier
from helper.hand_range_utils import HandRangeUtils
from helper.legal_action_resolver import LegalActionResolver
from helper.role_position_parser import RolePositionParser
from models.board_texture import BoardTexture
from models.poker_ml_input import PokerMLInput, FundamentalInputs, BetAction, VillainProfile
from models.poker_session import PokerSession
from services.game_dynamics_builder import GameDynamicsBuilder
from services.hand_range_service import HandRangeService
from services.psychological_context_builder import PsychologicalContextBuilder
from services.villain_profile_builder import VillainProfileBuilder


class InputVectorBuilder:
    def __init__(
        self,
        eval_service: Eval7Service,
        hand_classifier: HandClassifier,
        board_analyzer: BoardAnalyzer,
        position_analyzer: PositionAnalyzer,
        legal_action_resolver: LegalActionResolver,
        hand_range_service: HandRangeService,
        villain_profile_builder: VillainProfileBuilder,
        game_dynamics_builder: GameDynamicsBuilder,
        psychological_context_builder: PsychologicalContextBuilder,
    ):
        self.eval_service = eval_service
        self.hand_classifier = hand_classifier
        self.board_analyzer = board_analyzer
        self.position_analyzer = position_analyzer
        self.legal_action_resolver = legal_action_resolver
        self.hand_range_service = hand_range_service
        self.villain_profile_builder = villain_profile_builder
        self.game_dynamics_builder = game_dynamics_builder
        self.psychological_context_builder = psychological_context_builder

    def build(self, session: PokerSession) -> PokerMLInput:
        # 1. Build villain profiles for equity and downstream inputs
        villain_profiles = self.villain_profile_builder.build(session)

        # 2. Build fundamentals (including hero_equity_vs_range)
        fundamentals = self._build_fundamentals(session, villain_profiles)

        # 3. Build game dynamics and psychological context
        dynamics = self.game_dynamics_builder.build(session)
        psych = self.psychological_context_builder.build(session)

        return PokerMLInput(
            fundamentals=fundamentals,
            villain_profiles=villain_profiles,
            dynamics=dynamics,
            psych=psych,
        )

    def _build_fundamentals(
        self,
        session: PokerSession,
        villain_profiles: dict,
    ) -> FundamentalInputs:
        # Basic session state
        hero_hand = session.hero_hand
        board = session.board
        street = session.street
        pot_size = session.pot_size or 0.0
        stack = session.stack_sizes.get(session.hero_position, 0.0)
        spr = stack / pot_size if pot_size > 0 else 0.0

        # Analyze board and hand
        board_texture = self.board_analyzer.analyze(board)
        hand_strength = self.hand_classifier.classify(hero_hand, board)
        position_ctx = self.position_analyzer.analyze(session)

        # Determine legal actions
        is_all_in = stack <= 0.0
        bet_history = [
            BetAction(player=a.player, action=a.action, size=a.amount or 0.0)
            for a in session.action_history
            if a.action in {"bet", "raise", "call", "3bet", "shove"}
        ]
        legal_actions = self.legal_action_resolver.resolve(
            street=street,
            stack=stack,
            pot_size=pot_size,
            bet_history=bet_history,
            is_all_in=is_all_in,
        )

        # Calculate hero equity vs combined villain ranges
        equity = self._calculate_hero_equity(
            session=session,
            villain_profiles=villain_profiles,
            board_texture=board_texture,
        )

        return FundamentalInputs(
            hero_hand=hero_hand,
            board_cards=board,
            street=street,
            hero_position=session.hero_position,
            player_role=session.player_role,
            stack_to_pot_ratio=spr,
            pot_size=pot_size,
            effective_stack=stack,
            legal_actions=legal_actions,
            hero_equity_vs_range=equity,
            hero_hand_strength=hand_strength.label,
            board_texture=board_texture,
            position_context=position_ctx,
        )

    def _calculate_hero_equity(
            self,
            session: PokerSession,
            villain_profiles: Dict[str, VillainProfile],
            board_texture: BoardTexture
    ) -> float:
        board = session.board
        board_cluster_key = self.board_analyzer.get_cluster_id(board)
        board_str = "".join(board)

        parser = RolePositionParser(session.player_role)
        villain_positions = parser.get_villains()

        villain_ranges = []
        for pos in villain_positions:
            profile = villain_profiles.get(pos)
            if not profile:
                continue
            villain_range = self.hand_range_service.get_range(
                player_role=session.player_role,
                round=session.street,
                board=board_str,
                board_cluster=board_cluster_key,
                board_texture=board_texture,
                villain_profile=profile.to_dict(),  # or .to_dict() depending on implementation
            )
            if villain_range:
                villain_ranges.append(villain_range)

        merged_range = HandRangeUtils.merge_ranges(villain_ranges)

        return self.eval_service.calculate_equity(
            hero_hand=session.hero_hand,
            board=session.board,
            villain_range=merged_range
        )