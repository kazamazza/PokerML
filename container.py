from sqlalchemy.orm import Session

from analysis import hero_state_analyzer
from analysis.action_history_analyzer import ActionHistoryAnalyzer
from analysis.position_analyzer import PositionAnalyzer
from analysis.psychological_analyzer import PsychologicalAnalyzer
from analysis.session_context_analyzer import SessionContextAnalyzer
from analysis.villain.villain_history_analyzer import VillainHistoryAnalyzer
from board_analyzer import BoardAnalyzer
from board_clusterer import BoardClusterer
from board_normalizer import BoardNormalizer
from db.session import SessionLocal
from eval7_service import Eval7Service
from features.input_vector_builder import InputVectorBuilder
from hand_classifier.hand_classifier import HandClassifier
from helper.legal_action_resolver import LegalActionResolver
from services.game_dynamics_builder import GameDynamicsBuilder
from services.hand_range_service import HandRangeService
from services.psychological_context_builder import PsychologicalContextBuilder
from services.villain_profile_builder import VillainProfileBuilder
from villain_range_estimator import VillainRangeEstimator


class Container:
    def __init__(self):
        self._db_session = None

        # Singleton/shared services
        self._eval_service = None
        self._board_analyzer = None
        self._hand_classifier = None
        self._villain_estimator = None
        self._input_vector_builder = None
        self._board_normalizer = None
        self._board_clusterer = None

        # Advanced analyzers
        self._villain_history_analyzer = None
        self._action_history_analyzer = None
        self._position_analyzer = None
        self._range_comparator = None
        self._action_context_classifier = None
        self._tilt_risk_estimator = None
        self._opponent_aggregator = None

        self._psychological_analyzer = None
        self._hand_classifier = None
        self._legal_action_resolver = None
        self._hand_range_service =None

        self._villain_profile_builder = None
        self._game_dynamics_builder = None
        self._psychological_context_builder = None
        self._session_context_analyzer = None

    @property
    def db_session(self) -> Session:
        if self._db_session is None:
            self._db_session = SessionLocal()
        return self._db_session

    @property
    def board_normalizer(self) -> BoardNormalizer:
        if self._board_normalizer is None:
            self._board_normalizer = BoardNormalizer()
        return self._board_normalizer

    @property
    def eval_service(self) -> Eval7Service:
        if self._eval_service is None:
            self._eval_service = Eval7Service()
        return self._eval_service

    @property
    def board_clusterer(self) -> BoardClusterer:
        if self._board_clusterer is None:
            self._board_clusterer = BoardClusterer()
        return self._board_clusterer

    @property
    def board_analyzer(self) -> BoardAnalyzer:
        if self._board_analyzer is None:
            self._board_analyzer = BoardAnalyzer(board_clusterer=self.board_clusterer)
        return self._board_analyzer

    @property
    def hand_classifier(self) -> HandClassifier:
        if self._hand_classifier is None:
            self._hand_classifier = HandClassifier()
        return self._hand_classifier

    @property
    def villain_estimator(self) -> VillainRangeEstimator:
        if self._villain_estimator is None:
            self._villain_estimator = VillainRangeEstimator()
        return self._villain_estimator

    @property
    def villain_history_analyzer(self) -> VillainHistoryAnalyzer:
        if self._villain_history_analyzer is None:
            self._villain_history_analyzer = VillainHistoryAnalyzer()
        return self._villain_history_analyzer

    @property
    def action_history_analyzer(self) -> ActionHistoryAnalyzer:
        if self._action_history_analyzer is None:
            self._action_history_analyzer = ActionHistoryAnalyzer()
        return self._action_history_analyzer

    # Advanced analyzers
    @property
    def position_analyzer(self) -> PositionAnalyzer:
        if self._position_analyzer is None:
            self._position_analyzer = PositionAnalyzer()
        return self._position_analyzer

    @property
    def legal_action_resolver(self) -> LegalActionResolver:
        if self._legal_action_resolver is None:
            self._legal_action_resolver = LegalActionResolver()
        return self._legal_action_resolver

    @property
    def hand_range_service(self) -> HandRangeService:
        if self._hand_range_service is None:
            self._hand_range_service = HandRangeService(db_session=self.db_session)
        return self._hand_range_service

    @property
    def psychological_analyzer(self) -> PsychologicalAnalyzer:
        if self._psychological_analyzer is None:
            self._psychological_analyzer = PsychologicalAnalyzer()
        return self._psychological_analyzer

    @property
    def villain_profile_builder(self) -> VillainProfileBuilder:
        if self._villain_profile_builder is None:
            self._villain_profile_builder = VillainProfileBuilder(
                villain_history_analyzer=self.villain_history_analyzer,
                psychological_analyzer=self.psychological_analyzer,
            )
        return self._villain_profile_builder

    @property
    def game_dynamics_builder(self) -> GameDynamicsBuilder:
        if self._game_dynamics_builder is None:
            self._game_dynamics_builder = GameDynamicsBuilder(
                action_history_analyzer=self.action_history_analyzer
            )
        return self._game_dynamics_builder

    @property
    def session_context_analyzer(self) -> SessionContextAnalyzer:
        if self._session_context_analyzer is None:
            self._session_context_analyzer = SessionContextAnalyzer()
        return self._session_context_analyzer


    @property
    def psychological_context_builder(self) -> PsychologicalContextBuilder:
        if self._psychological_context_builder is None:
            self._psychological_context_builder = PsychologicalContextBuilder(
                session_context_analyzer=self.session_context_analyzer,
                board_analyzer=self._board_analyzer
            )
        return self._psychological_context_builder


    @property
    def input_vector_builder(self) -> InputVectorBuilder:
        if self._input_vector_builder is None:
            self._input_vector_builder = InputVectorBuilder(
                eval_service=self.eval_service,
                hand_classifier=self.hand_classifier,
                board_analyzer=self.board_analyzer,
                position_analyzer=self.position_analyzer,
                legal_action_resolver=self.legal_action_resolver,
                hand_range_service=self.hand_range_service,
                villain_profile_builder=self.villain_profile_builder,
                game_dynamics_builder=self.game_dynamics_builder,
                psychological_context_builder=self.psychological_context_builder,
            )
        return self._input_vector_builder