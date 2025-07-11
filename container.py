from sqlalchemy.orm import Session

from analysis.action_context_classifier import ActionContextClassifier
from analysis.action_history_analyzer import ActionHistoryAnalyzer
from analysis.opponent_model_aggregator import OpponentModelAggregator
from analysis.position_analyzer import PositionAnalyzer
from analysis.psychological_analyzer import PsychologicalAnalyzer
from analysis.range_strength_comparator import RangeStrengthComparator
from analysis.tilt_risk_estimator import TiltRiskEstimator
from board_analyzer import BoardAnalyzer
from board_clusterer import BoardClusterer
from board_normalizer import BoardNormalizer
from db.session import SessionLocal
from eval7_service import Eval7Service
from features.input_vector_builder import InputVectorBuilder
from hand_classifier.hand_classifier import HandClassifier
from helper.legal_action_resolver import LegalActionResolver
from services.hand_range_service import HandRangeService
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

    @property
    def db_session(self) -> Session:
        if not hasattr(self, "_db_session"):
            self._db_session = SessionLocal()
        return self._db_session

    @property
    def board_normalizer(self) -> BoardNormalizer:
        if self._board_normalizer is None:
            self._board_normalizer = BoardNormalizer()
        return self._board_normalizer

    @property
    def board_clusterer(self) -> BoardClusterer:
        if self._board_clusterer is None:
            self._board_clusterer = BoardClusterer()
        return self._board_clusterer

    @property
    def eval_service(self) -> Eval7Service:
        if self._eval_service is None:
            self._eval_service = Eval7Service()
        return self._eval_service

    @property
    def board_analyzer(self) -> BoardAnalyzer:
        if self._board_analyzer is None:
            self._board_analyzer = BoardAnalyzer()
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


    # Advanced analyzers

    @property
    def action_history_analyzer(self) -> ActionHistoryAnalyzer:
        if self._action_history_analyzer is None:
            self._action_history_analyzer = ActionHistoryAnalyzer()
        return self._action_history_analyzer

    @property
    def position_analyzer(self) -> PositionAnalyzer:
        if self._position_analyzer is None:
            self._position_analyzer = PositionAnalyzer()
        return self._position_analyzer

    @property
    def range_comparator(self) -> RangeStrengthComparator:
        if self._range_comparator is None:
            self._range_comparator = RangeStrengthComparator()
        return self._range_comparator

    @property
    def action_context_classifier(self) -> ActionContextClassifier:
        if self._action_context_classifier is None:
            self._action_context_classifier = ActionContextClassifier()
        return self._action_context_classifier

    @property
    def tilt_risk_estimator(self) -> TiltRiskEstimator:
        if self._tilt_risk_estimator is None:
            self._tilt_risk_estimator = TiltRiskEstimator()
        return self._tilt_risk_estimator

    @property
    def opponent_aggregator(self) -> OpponentModelAggregator:
        if self._opponent_aggregator is None:
            self._opponent_aggregator = OpponentModelAggregator()
        return self._opponent_aggregator

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
    def input_vector_builder(self) -> InputVectorBuilder:
        if self._input_vector_builder is None:
            self._input_vector_builder = InputVectorBuilder(
                eval_service=self.eval_service,
                hand_classifier=self.hand_classifier,
                board_analyzer=self.board_analyzer,
                villain_estimator=self.villain_estimator,
                position_analyzer=self.position_analyzer,
                action_history_analyzer=self.action_history_analyzer,
                psychological_analyzer=self.psychological_analyzer,
                hand_range_service=self.hand_range_service,
                legal_action_resolver=self.legal_action_resolver,
            )
        return self._input_vector_builder