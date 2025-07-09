import json
from typing import List
from board_normalizer import BoardNormalizer

class BoardClusterer:
    def __init__(self, path="data/board_textures.json"):
        with open(path, "r") as f:
            self.clusters = json.load(f)

        self.key_to_id = {key: idx for idx, key in enumerate(self.clusters.keys())}
        self.normalizer = BoardNormalizer()

    def get_cluster_id(self, board: List[str]) -> int:
        key = self.normalizer.normalize(board)
        return self.key_to_id.get(key, -1)  # -1 if unknown