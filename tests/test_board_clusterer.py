import pytest

from board_clusterer import BoardClusterer
from container import Container


@pytest.fixture
def container():
    return Container()


def test_board_clusterer_lazy_initialization_and_caching(container):
    # Before access, no BoardClusterer should exist
    assert getattr(container, "_board_clusterer", None) is None

    # First access should create a BoardClusterer
    bc1 = container.board_clusterer
    assert isinstance(bc1, BoardClusterer)
    # Should have loaded clusters from the default JSON
    assert isinstance(bc1.clusters, dict)
    assert isinstance(bc1.key_to_id, dict)
    # And should cache it on the private attribute
    assert getattr(container, "_board_clusterer") is bc1

    # Subsequent accesses return the same instance
    bc2 = container.board_clusterer
    assert bc2 is bc1

def test_board_clusterer_basic_normalization_and_id(container, tmp_path, monkeypatch):
    # Prepare a minimal clusters JSON file
    clusters = {
        "2-4-5:connected:rainbow": [],
        "Q-K-A:connected:monotone": []
    }
    json_path = tmp_path / "board_textures.json"
    json_path.write_text(json.dumps(clusters))

    # Point the BoardClusterer to our test JSON
    monkeypatch.setenv("PROJECT_ROOT", str(tmp_path.parent))
    # When container instantiates, it will pick up path = PROJECT_ROOT/config/board_textures.json
    config_dir = tmp_path.parent / "config"
    config_dir.mkdir(exist_ok=True)
    (config_dir / "board_textures.json").write_text(json.dumps(clusters))

    # Re-create the clusterer to pick up our test file
    # Clear the cached instance
    container._board_clusterer = None
    bc = container.board_clusterer

    # Test that normalize delegates to BoardNormalizer
    norm = bc.get_cluster_key(["2h", "4d", "5s"])
    assert norm == "2-4-5:connected:rainbow"

    # Test that get_cluster_id returns the correct index
    idx = bc.get_cluster_id(["2h", "4d", "5s"])
    assert idx == list(clusters.keys()).index("2-4-5:connected:rainbow")

    # And unknown boards yield -1
    assert bc.get_cluster_id(["Ah", "Kd", "Qs"]) == -1