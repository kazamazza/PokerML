import pytest

from board_normalizer import BoardNormalizer


@pytest.fixture
def normalizer():
    return BoardNormalizer()


@pytest.mark.parametrize(
    "board, expected",
    [
        # Triplet + rainbow (3 suits)
        (["Ah", "Ad", "Ac"], "A-A-A:triplet:rainbow"),

        # Paired + twotone (2 suits)
        (["Ah", "Ad", "2h"], "2-A-A:paired:twotone"),

        # Uncoordinated + rainbow
        (["As", "7d", "Kh"], "7-K-A:uncoordinated:rainbow"),

        # Connected + rainbow
        (["2h", "4d", "5s"], "2-4-5:connected:rainbow"),

        # Connected + monotone (all hearts)
        (["Ah", "Kh", "Qh"], "Q-K-A:connected:monotone"),
    ]
)
def test_normalize_various_boards(normalizer, board, expected):
    result = normalizer.normalize(board)
    assert result == expected