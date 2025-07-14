import pytest

from board_analyzer import BoardAnalyzer
from board_normalizer import BoardNormalizer


@pytest.fixture
def board_analyzer():
    return BoardAnalyzer()


def test_board_normalizer_lazy_initialization_and_caching(board_analyzer):
    # Initially, the private attribute should be None
    assert getattr(board_analyzer, "_board_normalizer") is None

    # First access should create a BoardNormalizer instance
    first = board_analyzer.board_normalizer
    assert isinstance(first, BoardNormalizer)
    # And store it in the private attribute
    assert getattr(board_analyzer, "_board_normalizer") is first

    # Further accesses should return the same object (cached)
    second = board_analyzer.board_normalizer
    assert second is first