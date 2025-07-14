import pytest

from board_analyzer import BoardAnalyzer
from models.board_texture import BoardTexture


class DummyClusterer:
    def get_cluster_id(self, board):
        return 99
    def get_cluster_key(self, board):
        return "dummy"


@pytest.fixture
def analyzer():
    # inject a dummy clusterer so we can assert on board_cluster_id
    return BoardAnalyzer(board_clusterer=DummyClusterer())


def test_analyze_empty_board_returns_empty_texture(analyzer):
    tex = analyzer.analyze([])
    assert isinstance(tex, BoardTexture)
    # empty‐texture defaults
    assert tex.board_class == "empty"
    assert tex.structure == "uncoordinated"
    assert tex.suit_texture == "rainbow"
    assert tex.board_cluster_id == 0  # from _empty_texture


def test_analyze_simple_connected_rainbow(analyzer):
    board = ["Ah", "Kd", "Qs"]
    tex = analyzer.analyze(board)

    # ranks A,K,Q → connected
    assert tex.structure == "connected"
    # three different suits → rainbow
    assert tex.suit_texture == "rainbow"
    # high card is Ace → 14
    assert tex.high_card_rank == 14
    # connectivity flags
    assert tex.is_connected is True
    assert tex.is_paired is False
    # no flush draw on 3‐card rainbow
    assert tex.has_flush_draw is False
    # straight draw (A,K,Q) yields True
    assert tex.has_straight_draw is True
    # no backdoor straight draw
    assert tex.has_backdoor_straight_draw is False
    # board_class falls back to Generic
    assert tex.board_class == "Generic"
    # dummy clusterer always returns 99
    assert tex.board_cluster_id == 99

    # texture‐blocker influence: connected → 0.8
    assert pytest.approx(tex.texture_blocker_influence_score, rel=1e-3) == 0.8
    # coordination density: connected(.4)+straight_draw(.3) = .7
    assert pytest.approx(tex.coordination_density_score, rel=1e-3) == 0.7


def test_analyze_monotone_connected_with_flush_draw_and_full_scores(analyzer):
    board = ["Ah", "Kh", "Qh"]
    tex = analyzer.analyze(board)

    # ranks A,K,Q → connected
    assert tex.structure == "connected"
    # all same suit → monotone
    assert tex.suit_texture == "monotone"
    # flush‐draw on flop monotone
    assert tex.has_flush_draw is True
    # flush possible only on 5+ cards
    assert tex.is_flush_possible is False
    # no backdoor flush (needs exactly two of same suit when len>=3)
    assert tex.has_backdoor_flush_draw is False
    # two‐tone is false
    assert tex.is_two_tone is False  # you might need to add this property if missing

    # texture‐blocker: connected(.8) + monotone(.2) = 1.0
    assert pytest.approx(tex.texture_blocker_influence_score, rel=1e-3) == 1.0
    # coordination density: connected(.4) + flush_draw(.3) = .7
    assert pytest.approx(tex.coordination_density_score, rel=1e-3) == 0.7