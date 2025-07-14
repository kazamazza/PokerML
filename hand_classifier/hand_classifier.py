from typing import List

from hand_classifier.classification_context import ClassificationContext
from hand_classifier.detectors.combo_draw_detector import ComboDrawDetector
from hand_classifier.detectors.flush_detector import FlushDetector
from hand_classifier.detectors.full_house_detector import FullHouseDetector
from hand_classifier.detectors.one_pair_detector import OnePairDetector
from hand_classifier.detectors.quads_detector import QuadsDetector
from hand_classifier.detectors.set_detector import SetDetector
from hand_classifier.detectors.straight_detector import StraightDetector
from hand_classifier.detectors.trips_detector import TripsDetector
from hand_classifier.detectors.two_pair_detector import TwoPairDetector
from models.board_texture import BoardTexture
from models.hand_context import HandContext
from models.hand_strength import HandStrength, HandCategory


class HandClassifier:
    def __init__(self):
        self.detectors = [
            QuadsDetector(),
            FullHouseDetector(),
            SetDetector(),
            TripsDetector(),
            TwoPairDetector(),
            OnePairDetector(),
            FlushDetector(),
            StraightDetector(),
            ComboDrawDetector()
        ]

    def classify(self, hero_hand: List[str], board: List[str], board_texture: BoardTexture = None) -> HandStrength:
        hand_ctx = HandContext(hero_hand, board, board_texture)
        classification_ctx = ClassificationContext.from_hand_context(hand_ctx)

        for detector in self.detectors:
            result = detector.detect(classification_ctx)
            if result is not None:
                return result

        return HandStrength(HandCategory.HIGH_CARD)