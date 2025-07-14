import pytest

from hand_classifier.hand_classifier import HandClassifier
from models.hand_strength import HandStrength, HandCategory


@pytest.fixture
def classifier():
    return HandClassifier()


@pytest.mark.parametrize(
    "hero_hand, board, expected_label",
    [
        (["Ah", "Ad"], ["Ac", "As", "2d"], "Quads"),
        (["Kh", "Kd"], ["Kc", "Qs", "Qd"], "Full House"),
        (["5h", "5d"], ["5c", "9s", "2d"], "Set"),
        (["Ah", "Kd"], ["7c", "7s", "7d"], "Trips"),
        (["Jh", "Jd"], ["9c", "9s", "2d"], "Two Pair"),
        (["Th", "Td"], ["3c", "8s", "2d"], "One Pair"),
        (["2h", "7h"], ["Kh", "8h", "9h"], "Flush"),
        (["2h", "3d"], ["4s", "5c", "6h"], "Straight"),
        (["Ah", "2d"], ["3s", "4c", "9h"], "High Card"),
    ]
)
def test_classify_all_strengths(classifier, hero_hand, board, expected_label):
    result: HandStrength = classifier.classify(hero_hand, board)
    # It should return the new HandStrength type
    assert isinstance(result, HandStrength)
    # The label should be one of our HandCategory values
    assert isinstance(result.label, HandCategory)
    # And its string value should match the expected text
    assert result.label.value == expected_label